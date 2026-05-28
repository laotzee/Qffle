from cli import sort_cards


def test_sort_cards(mock_content_deck):

    test_set = set(mock_content_deck.cards)

    sorted_list = sort_cards(test_set)

    assert sorted_list[0].question.startswith("How many")
    assert sorted_list[1].question.startswith("What is")
