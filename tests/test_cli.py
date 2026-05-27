from db import Card
from cli import sort_cards


def test_sort_cards():

    card1 = Card("What is the German word for 'Bread'?", "Das Brot")
    card2 = Card("How many days does a year typically have?", "365")
    test_set = {card1, card2}

    sorted_list = sort_cards(test_set)

    assert sorted_list[0].question == card2.question
    assert sorted_list[1].question == card1.question
