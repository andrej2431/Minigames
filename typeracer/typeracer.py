import time
import random


def text_to_words(text):
    words = text.replace(".", "").replace(",", "").split()
    return words


def calculate_wpm(words, start, end, number_of_errors=0):
    minutes_taken = (end - start) / 60
    gross_wpm = (len("".join(words)) / 5) / minutes_taken
    net_wpm = round(gross_wpm - number_of_errors / minutes_taken)
    return net_wpm if net_wpm > 0 else 0


def generate_random_text():
    text_file = open("random_text.txt", "r")
    possible_texts = []
    for line in text_file:
        possible_texts.append(line)
    return random.choice(possible_texts)


def timed_random_text():
    text = generate_random_text()
    print(text,end="")
    typed_text = ""
    start = time.time()
    text = input()
    end = time.time()

    words = text_to_words(text)
    number_of_errors = len([typed for correct, typed in zip(text, typed_text) if typed != correct])
    wpm = calculate_wpm(words, start, end, number_of_errors=number_of_errors)
    print(f"{len(words)} words typed in {round(end - start, 2)} seconds. You typed at {wpm} words per minute.")


def timed_typed_text():
    start = time.time()
    text = input()
    end = time.time()

    words = text_to_words(text)
    wpm = calculate_wpm(words, start, end)
    print(f"{len(words)} words typed in {round(end - start, 2)} seconds. You typed at {wpm} words per minute.")


def main():
    print("Welcome to Typeracer, interactive game that tests your typing speed!")

    while True:

        command = input("Type 1 if you want to time a random text, type 2 if you want to time your own text,"
                        " type exit to end the game: ")
        if command == "1":
            timed_random_text()
        elif command == "2":
            timed_typed_text()
        elif command == "exit":
            break
        else:
            print("Please use valid commands.")


main()
