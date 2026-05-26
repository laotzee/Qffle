import csv
import datetime
from db import Deck, Card, ContentDeck, db_session
from sqlalchemy import select
from db import Session

FILE_PATH = "resources/most_used_german_words.csv"
READ_MAX = 10000


def create_card(card_data: list):
    """Returns a Card from the card_data. If card_data is not a pair, an empty
    string will be used as placeholder"""
    if len(card_data) < 2:
        card_data.append("")
    return Card(question=card_data[0], answer=card_data[1])


def read_cards(file: str) -> ContentDeck | None:
    """Returns the contents of a csv file with question-answer pairs as a
    DeckContent instance, or None if the file had not the .csv extention or
    did not exist"""

    if file[-4:].lower() != ".csv":
        return None

    try:
        with open(file) as read_file:
            reader = csv.reader(read_file)
            headings = next(reader)
            cards = []
            for card_data in reader:
                if card_data:
                    cards.append(create_card(card_data))

            deck_content = ContentDeck(
                question_header=headings[0],
                answer_header=headings[1],
                cards=cards,
            )
            return deck_content
    except FileNotFoundError:
        return None


def get_deck_by_path(search_path: str) -> Deck | None:
    """
    Looks up a deck by its path.
    Returns the Deck instance if found, otherwise None.
    """
    stmt = select(Deck).where(Deck.path == search_path)
    return db_session.execute(stmt).scalar_one_or_none()


def update_deck(deck: Deck, current_count: int) -> None:
    """
    Updates a decks 'last_visited' timestamp and its items if they differ from
    the record
    """
    deck.last_visited = datetime.datetime.now(datetime.UTC)
    if current_count != deck.item_count:
        deck.item_count = current_count

    db_session.add(deck)
    db_session.commit()


def create_deck(path: str, items: int = 0) -> Deck:
    """
    Creates a new deck entry in the database.
    """
    new_deck = Deck(path=path, item_count=items)
    db_session.add(new_deck)
    db_session.commit()
    db_session.refresh(new_deck)
    return new_deck


def create_session(
    deck: Deck,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    errors: int,
    is_inverted: bool,
) -> Session:
    """
    Calculates duration, creates a new session linked to a deck, and saves it.
    """
    delta = end_time - start_time

    seconds = int(delta.total_seconds())
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"

    new_session = Session(
        duration=duration_str,
        errors=errors,
        item_count=deck.item_count,
        deck_id=deck.id,
        is_inverted=is_inverted,
    )

    db_session.add(new_session)
    db_session.commit()
    db_session.refresh(new_session)

    return new_session


def get_best_session(deck_id: int, is_inverted: bool) -> Session | None:
    """
    Returns the session instance with the shortest duration
    for a specific deck. Returns None if no sessions exist.
    """
    stmt = (
        select(Session)
        .where(Session.deck_id == deck_id)
        .where(Session.is_inverted == is_inverted)
        .order_by(
            Session.item_count.desc(),
            Session.errors.asc(),
            Session.duration.asc(),
            Session.created_at.desc(),
        )
        .limit(1)
    )

    return db_session.execute(stmt).scalar_one_or_none()


if __name__ == "__main__":
    words = read_cards(FILE_PATH)
#    count = 0
#    for row in words:
#        count += 1
#        print(row)
#        if count > 10:
#            break
