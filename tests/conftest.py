import pytest
import datetime
from db import Card, ContentDeck, Session


@pytest.fixture()
def mock_content_deck():
    card1 = Card(
        question="What is the German word for 'Bread'?",
        answer="Das Brot",
    )
    card2 = Card(
        question="How many days does a year typically have?",
        answer="365",
    )
    data = ContentDeck(
        question_header="Question",
        answer_header="Answer",
        cards=[card1, card2],
    )
    return data


@pytest.fixture()
def mock_sessions():
    session1 = Session(
        duration="00:02:01",
        errors=5,
        item_count=43,
        deck_id=1,
        created_at=datetime.datetime.now(),
    )
    session2 = Session(
        duration="00:04:01",
        errors=5,
        item_count=83,
        deck_id=2,
        created_at=datetime.datetime.now(),
    )

    return [session1, session2]
