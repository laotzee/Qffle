import csv
from random import shuffle
from typing import Tuple

FILE_PATH = "resources/most_used_german_words.csv"
READ_MAX = 10000

def read_cards(file):
    """Returns the contents of a csv file as X"""

    if type(file) == tuple:
        return file
    elif file[-4:].lower() != ".csv":
        return file

    with open(file) as read_file: #I need to put a guard here

        reader = csv.reader(read_file)
        cards = {
            "headings": next(reader),
            "cards": []}

        for row in reader:
            if len(row) < 2: row.append("")
            cards["cards"].append((row[0], row[1]))
            if count == READ_MAX:
                return cards
        return cards

def shuffle_cards(cards):
    """Randomize the order of the cards """

    if type(cards) == dict:
        shuffle(cards["cards"])

if __name__ == "__main__":


    words = read_cards(FILE_PATH)
#    count = 0
#    for row in words:
#        count += 1
#        print(row)
#        if count > 10:
#            break
