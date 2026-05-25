import os
import sys
import datetime
from cards import (
    create_deck,
    get_deck_by_path,
    read_cards,
    create_session,
    update_deck,
    get_best_session,
)
from db import Deck, ContentDeck, Session


def sort_cards(s: set) -> list:
    """Returns a list containing all the elements of a set of cards sorted
    alphabetically by their question"""
    sorted_list = list(s)
    sorted_list.sort(key=lambda card: card.question)
    return sorted_list


def report_errors(error_cards: set):

    if error_cards:
        sorted_cards = sort_cards(error_cards)
        print("Cards you may want to review for next session")
        print("-------------------------------------\n")
        for card in sorted_cards:
            print(f"{card.question} -----> {card.answer}")
        print("\n-------------------------------------")


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


def start_session(deck: Deck, deck_content: ContentDeck):
    """Shows the user a given deck to memorize its cards"""

    points = 0
    mistakes = 0
    pending_cards = []
    error_cards = set()

    inverse = input("(1) regular (2) inverse\n")
    if inverse == "2":
        deck_content.reverse_order()

    start = datetime.datetime.now()
    while deck_content.cards:
        clear_screen()
        if pending_cards:
            card = pending_cards.pop()
            print("Invalid input, just use 1 or 0")
        else:
            card = deck_content.next()
        print("================================\n")
        print(f"{deck_content.question_header}\n")
        print(f"{card.question}\n")

        input()

        print(f"{deck_content.question_header} -----> {deck_content.answer_header}\n")
        print(f"{card.question} -----> {card.answer}\n")
        print("================================\n")

        answer = input("(1) Right (2) Wrong\n")
        if answer.isdigit() and answer == "1":
            points += 1
        elif answer.isdigit() and answer == "2":
            deck_content.cards.append(card)
            deck_content.shuffle()
            error_cards.add(card)
            mistakes += 1
        else:
            pending_cards.append(card)

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
if not deck_content:
    print("File must exist and have a .csv extention")
    exit()

deck = get_deck_by_path(file)

if deck:
    update_deck(deck, deck_content.deck_len)
else:
    deck = create_deck(file, deck_content.deck_len)

start_session(deck, deck_content)
