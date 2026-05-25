import datetime
from random import shuffle
from typing import List
from sqlalchemy import Boolean, create_engine, ForeignKey, DateTime, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Card:
    """Models the question and answer sides of a card"""

    def __init__(self, question: str, answer: str) -> None:
        self.question = question
        self.answer = answer

    def swap_places(self):
        """Answer and question change places"""
        self.question, self.answer = self.answer, self.question
        return self


class ContentDeck:
    """Models the content of a deck"""

    def __init__(
        self,
        question_header: str,
        answer_header: str,
        cards: list[Card],
    ) -> None:
        self.question_header = question_header
        self.answer_header = answer_header
        self.cards = cards
        self.deck_len = len(self.cards)
        self.shuffle()

    def reverse_order(self):
        """Flips the order of the cards"""
        self.question_header, self.answer_header = (
            self.answer_header,
            self.question_header,
        )
        for card in self.cards:
            card.swap_places()
        return self

    def next(self) -> Card:
        """Return the next Card"""
        return self.cards.pop()

    def shuffle(self):
        return shuffle(self.cards)


class Deck(Base):
    """Models a deck of cards"""

    __tablename__ = "decks"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    path: Mapped[str] = mapped_column(nullable=False, index=True)
    last_visited: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.now()
    )
    item_count: Mapped[int] = mapped_column(default=0)

    sessions: Mapped[List["Session"]] = relationship("Session", back_populates="deck")


class Session(Base):
    """Models a study session"""

    __tablename__ = "sessions"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    duration: Mapped[str]
    errors: Mapped[int] = mapped_column(default=0)
    item_count: Mapped[int] = mapped_column(default=0)
    deck_id: Mapped[int] = mapped_column(ForeignKey("decks.id"))
    created_at: Mapped[datetime.datetime] = mapped_column(
        insert_default=func.now(),
    )

    deck: Mapped["Deck"] = relationship("Deck", back_populates="sessions")
    is_inverted: Mapped[bool] = mapped_column(default=False)


def init_db():
    Base.metadata.create_all(bind=engine)


init_db()

db_session = SessionLocal()
