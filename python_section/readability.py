import re
import math

def get_string(prompt):
    # User text input and return it
    return input(prompt)

def count_letters(text):
    # count the number of letters
    return len(re.findall(r'[a-zA-Z]', text))

def count_words(text):
    # count number of words in the text
    return len(re.findall(r'\b[\w\'\-]+\b', text))

def count_sentences(text):
    # count the number of sentences based on punctuation marks
    return len(re.findall(r'[.!?]', text))

def coleman_liau_index(letters, words, sentences):
    L = (letters / words) * 100
    S = (sentences / words) * 100
    index = (0.0588 * L) - (0.29 * S) - 15.8
    return round(index)

def main():
    text = get_string("Text: ")

    number_of_letters = count_letters(text)
    print(number_of_letters)
    number_of_words = count_words(text)
    print(number_of_words)
    number_of_sentences = count_sentences(text)
    print(number_of_sentences)
    index = coleman_liau_index(number_of_letters, number_of_words, number_of_sentences)

    # print the grade
    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")

main()
