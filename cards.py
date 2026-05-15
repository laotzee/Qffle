import csv
from db import Deck, db_session
from sqlalchemy import select
from random import shuffle
from typing import Tuple

FILE_PATH = "resources/most_used_german_words.csv"
READ_MAX = 10000


def create_card(text_pair: list):
    """Returns a tuple containing two strings of a card. If pair is missing
    an empty value takes its place"""
    if len(text_pair) < 2:
        text_pair.append("")
    return (text_pair[0], text_pair[1])


def read_cards(file):
    """Returns the contents of a csv file as X"""

    if type(file) == tuple:
        return file
    elif file[-4:].lower() != ".csv":
        return file

    with open(file) as read_file:  # I need to put a guard here
        reader = csv.reader(read_file)
        cards = {"headings": next(reader), "cards": []}
        for row in reader:
            cards["cards"].append(create_card(row))
        return cards


def shuffle_cards(cards):
    """Randomize the order of the cards"""

    if type(cards) == dict:
        shuffle(cards["cards"])


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
    deck: Deck, start_time: datetime.datetime, end_time: datetime.datetime, errors: int
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
    )

    db_session.add(new_session)
    db_session.commit()
    db_session.refresh(new_session)

    return new_session


if __name__ == "__main__":
    words = read_cards(FILE_PATH)
#    count = 0
#    for row in words:
#        count += 1
#        print(row)
#        if count > 10:
#            break
