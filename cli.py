import os
import sys
import datetime
from cards_bak import (
    create_deck,
    get_deck_by_path,
    read_cards,
    shuffle_cards,
    create_session,
    update_deck,
    get_best_session,
)
from db import Deck, Session


def sort_set(s) -> list:
    """Returns a list containing all the elements of the set sorted
    alphabetically"""
    sorted_list = list(s)
    sorted_list.sort()
    return sorted_list


def report_errors(error_cards: set):

    if error_cards:
        sorted_cards = sort_set(error_cards)
        print("Cards you may want to review for next session")
        print("-------------------------------------")
        for card in sorted_cards:
            print(card)
        print("-------------------------------------")


def compare_sessions(current_session: Session, best_session: Session):
    """Prints a report comparing the total cards, mistakes, and duration
    of the two sessions"""

    print("---------- Current Session ----------\n")
    print(f"Total cards: {current_session.item_count}")
    print(f"Mistakes: {current_session.errors}")
    print(f"Duration: {current_session.duration}\n")

    print("-------------------------------------")
    print("------------ Best Session -----------\n")
    print(f"Total cards: {best_session.item_count}")
    print(f"Mistakes: {best_session.errors}")
    print(f"Duration: {best_session.duration}\n")
    print("-------------------------------------")


def start_session(deck: Deck, deck_content):
    """Shows the user a given deck to memorize its cards"""

    headings = deck_content["headings"]
    cards = deck_content["cards"]
    points = 0
    mistakes = 0
    pending_cards = []
    error_cards = set()
    question_header = headings[0]
    answer_header = headings[1]

    start = datetime.datetime.now()
    while cards:
        clear_screen()
        if pending_cards:
            card = pending_cards.pop()
            print("Invalid input, just use 1 or 0")
        else:
            card = cards.pop(0)
        print("================================\n")
        print(f"{question_header}\n")
        print(f"{card[0]}\n")

        input()

        print(f"{question_header} -----> {answer_header}\n")
        print(f"{card[0]} -----> {card[1]}\n")
        print("================================\n")

        answer = input("(1) Right (2) Wrong\n")
        if answer.isdigit() and answer == "1":
            points += 1
        elif answer.isdigit() and answer == "2":
            cards.append(card)
            error_cards.add(card)
            mistakes += 1
        else:
            pending_cards.append(card)
            continue

    end = datetime.datetime.now()

    current_session = create_session(
        deck=deck,
        start_time=start,
        end_time=end,
        errors=len(error_cards),
    )

    best_session = get_best_session(deck_id=deck.id)
    report_errors(error_cards)
    compare_sessions(current_session, best_session)


def clear_screen():
    # For Windows
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


args = sys.argv
file = args[1] if len(args) > 1 else None

if not file:
    file = input("Absolute path for the cards: ")

deck_content = read_cards(file)
shuffle_cards(deck_content)
deck_len = len(deck_content["cards"])

deck = get_deck_by_path(file)
if deck:
    update_deck(deck, deck_len)
else:
    deck = create_deck(file, deck_len)

start_session(deck, deck_content)
