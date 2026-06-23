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
    get_last_files,
)
from db import Deck, ContentDeck, Session, Card

SEPARATOR = "----->"


def sort_cards(s: set[Card]) -> list[Card]:
    """Returns a list containing all the elements of a set of cards sorted
    alphabetically by their question"""

    sorted_list = list(s)
    sorted_list.sort(key=lambda card: card.question)
    return sorted_list


def error_report(error_cards: set[Card]):
    """Returns a formatted string containing all the cards within
    error_cards"""
    report = [
        "Cards you may want to review for next session",
        "-------------------------------------\n",
    ]
    sorted_cards = sort_cards(error_cards)
    for card in sorted_cards:
        report.append(f"{card.question} {SEPARATOR} {card.answer}\n")
    report.append("\n-------------------------------------")
    return "".join(report)


def session_report(current_session: Session, best_session: Session | None):
    """Returns a report that compares the total cards, mistakes, and duration
    of the two sessions. If not best_session, the current_session is displayed
    as the best one"""

    compare_session = best_session if best_session else current_session

    report = [
        "---------- Current Session ----------\n",
        f"Total cards: {current_session.item_count}\n",
        f"Mistakes: {current_session.errors}\n",
        f"Duration: {current_session.duration}\n",
        "-------------------------------------\n",
        "------------ Best Session -----------\n",
        f"Total cards: {compare_session.item_count}\n",
        f"Mistakes: {compare_session.errors}\n",
        f"Duration: {compare_session.duration}\n",
        "-------------------------------------",
    ]
    return "".join(report)


def start_session(deck: Deck, deck_content: ContentDeck):
    """Shows the user a given deck to memorize its cards"""

    points = 0
    mistakes = 0
    pending_cards = []
    reports = []
    error_cards = set()
    is_inverted = False

    inverse = input("(1) regular (2) inverse\n")
    if inverse == "2":
        deck_content.reverse_order()
        is_inverted = True

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
        is_inverted=is_inverted,
    )

    best_session = get_best_session(deck_id=deck.id, is_inverted=is_inverted)
    if error_cards:
        reports.append(error_report(error_cards))
    reports.append(session_report(current_session, best_session))

    for report in reports:
        print(report)


def clear_screen():
    # For Windows
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def last_files_menu() -> str | None:
    """Returns the absolute path of the chosen file, or None if the user picks
    an invalid option"""
    answers = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
    ]
    files = get_last_files()
    files_len = len(files)
    valid_answers = answers[: files_len + 1]
    last_option = files_len
    if files:
        print("Select a file to start:\n")

        for num, file in enumerate(files):
            print(f"{num}) {file.path}\n")
        print(f"{last_option}) Exit\n")

        option = input("")
        print(option)
        if option.isdigit() and option in valid_answers:
            option = int(option)
            if option == last_option:
                exit()
            else:
                file = files[option]
                return file.path
        else:
            return None
    else:
        pass


if __name__ == "__main__":
    args = sys.argv
    path = args[1] if len(args) > 1 else None

    if not path:
        path = last_files_menu()

    if path is None:
        print("Invalid option selected")
        exit()

    deck = get_deck_by_path(path)
    deck_content = read_cards(path)

    if not deck_content:
        print("File not found, or not properly formatted")
        exit()

    if deck:
        update_deck(deck, deck_content.deck_len)
    else:
        deck = create_deck(path, deck_content.deck_len)

    start_session(deck, deck_content)
