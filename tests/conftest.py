import pytest
from db import Card, ContentDeck


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
