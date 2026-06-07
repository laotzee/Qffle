from sqlalchemy.engine import mock
from cli import (
    session_report,
    sort_cards,
    SEPARATOR,
    error_report,
)


def test_sort_cards(mock_content_deck):

    test_set = set(mock_content_deck.cards)

    sorted_list = sort_cards(test_set)

    assert sorted_list[0].question.startswith("How many")
    assert sorted_list[1].question.startswith("What is")


def test_session_report(mock_sessions):
    """Test that every piece of the report corresponds with the data inside
    the respective sessions"""

    properties_to_test = [
        ["item_count", "Total cards:"],
        ["errors", "Mistakes:"],
        ["duration", "Duration:"],
    ]
    test_sessions = mock_sessions[:2]
    report = session_report(test_sessions[0], test_sessions[1])

    for session in test_sessions:
        for attr_name, label in properties_to_test:
            value = getattr(session, attr_name)
            assert f"{label} {value}" in report


def test_error_report(mock_content_deck):
    """Test that every piece of the report corresponds with the data inside
    the respective sessions"""

    mock_error_cards = set(mock_content_deck.cards.copy())
    report = error_report(mock_error_cards)

    for card in mock_error_cards:
        assert f"{card.question} {SEPARATOR} {card.answer}" in report
