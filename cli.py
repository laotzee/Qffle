import os
from cards import read_cards, shuffle_cards


def clear_screen():
    # For Windows
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


file = input("Absolute path for the cards: ")

deck = read_cards(file)
shuffle_cards(deck)
headings = deck["headings"]
cards = deck["cards"]

points = 0
mistakes = 0
pending_cards = []
total_cards = len(cards)
question_header = headings[0]
answer_header = headings[1]

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
        mistakes += 1
    else:
        pending_cards.append(card)
        continue


print(f"Total cards: {total_cards}")
print(f"Score: {points}")
print(f"Mistakes: {mistakes}")
