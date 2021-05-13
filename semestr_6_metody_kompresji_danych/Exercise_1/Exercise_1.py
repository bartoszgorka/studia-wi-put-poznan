import numpy as np
import operator
import random


# Exercise 1 - Generate words and calculate average length.
def exercise_1(size):
    alphabet = list("qazxswedcvfrtgbnhyujmkilop ")
    total_length = 0
    for _ in range(size):
        total_length += len(exercise_1_single_word(alphabet))

    return total_length / size


# Single word - Example 1 generator.
def exercise_1_single_word(alphabet):
    word = ""
    while True:
        char = np.random.choice(alphabet)
        if char != " ":
            word += char
        else:
            break
    return word


# Read file's content
def read_file(name):
    file = open(name, 'r')
    return file.read()


# Calculate file details, return average characters length in file.
def file_parameters(filename):
    content = read_file(filename)
    total_length = 0
    words = content.split(" ")

    for word in words:
        total_length += len(word)

    return total_length / len(words)


# Exercise 2 - Calculate frequency of letters in text.
def exercise_2(filename):
    content = read_file(filename)
    letters = {}
    counter = 0

    for _, letter in enumerate(content):
        cardinality = letters.get(letter, 0)
        letters.update({letter: cardinality + 1})
        counter += 1

    for letter in letters:
        letters.update({letter: letters.get(letter) / counter})

    return letters


# Exercise 3 - Calculate first row average length.
def exercise_3(size, frequency):
    keys = list(frequency.keys())
    probability_list = list(frequency.values())
    total_length = 0

    for _ in range(size):
        total_length += len(exercise_3_word_generator(keys, probability_list))

    return total_length / size


# Words generator - Exercise 3.
def exercise_3_word_generator(alphabet, probability):
    word = ""
    while True:
        char = np.random.choice(alphabet, p=probability)
        if char != " ":
            word += char
        else:
            break
    return word


# Exercise 4 - Probability of letters in text.
def exercise_4(filename):
    content = read_file(filename)
    letters = {}
    counter = 0
    old_letter = ""

    for _, letter in enumerate(content):
        if old_letter != "":
            dictionary_item = letters.get(old_letter, {})
            cardinality = dictionary_item.get(letter, 0)
            cardinality_total = dictionary_item.get("total", 0)

            dictionary_item.update({letter: cardinality + 1})
            dictionary_item.update({"total": cardinality_total + 1})
            letters.update({old_letter: dictionary_item})
            counter += 1
        old_letter = letter

    return letters, counter


# Modify dictionaries.
def modify_dictionaries(dictionary, top_key, key):
    selected = dictionary.get(top_key, {})
    value = selected.get(key, 0)
    total = selected.get("total", 0)

    selected.update({key: value + 1})
    selected.update({"total": total + 1})
    dictionary.update({top_key: selected})

    return dictionary


# Exercise 5 - Analyze files, calculate file's statistics.
def exercise_5_analyze(filename, row):
    content = read_file(filename)
    dictionary = {}
    letters = []

    for _, letter in enumerate(content):
        if len(letters) > row:
            del(letters[0])
            dictionary = modify_dictionaries(dictionary, ''.join(letters), letter)
        letters.append(letter)

    return dictionary


# Roulette wheel
def roulette_wheel(letters, probability):
    value = random.random()
    probability_sum = 0.0
    selected = 0

    for ind, val in enumerate(probability):
        probability_sum += val
        if probability_sum >= value:
            selected = ind
            break

    return letters[selected]


# Exercise 5 - generator with use roulette wheel and statistics from file.
def exercise_5_generator(dictionary, row, length):
    result = "probability"
    letters = list(result)
    for _ in range(len(letters) - row):
        del(letters[0])

    for i in range(length):
        letters_to_random = list()
        probability_to_random = list()

        selected = dictionary.get(''.join(letters))
        total = selected.get("total", 1)

        for (key, value) in selected.items():
            if key != "total":
                letters_to_random.append(key)
                probability_to_random.append(value / total)

        if probability_to_random:
            char = roulette_wheel(letters_to_random, probability_to_random)
        else:
            char = np.random.choice(list("qazxswedcvfrtgbnhyujmkilop "))

        result += char

        letters.append(char)
        if len(letters) > row:
            del(letters[0])

    return result


# Main function
def main():
    # File details
    print("File details:")
    files = ["norm_hamlet.txt", "norm_romeo_and_juliet.txt", "norm_wiki_sample.txt"]
    for filename in files:
        print("\tFile =", filename, "\tAverage length =", file_parameters(filename), "characters")

    # Exercise 1
    words_size = 2000
    print("\nExercise 1:\n\tWords =", words_size, "\tAverage length =", exercise_1(words_size), "characters")

    # Exercise 2
    frequency = {}
    print("\nExercise 2:")
    for filename in files:
        frequency = exercise_2(filename)
        print("\tFile =", filename, "\tLetters:", frequency)

    # Exercise 3
    print("\nExercise 3:\n\tWords = ", words_size, "\tAverage length =", exercise_3(words_size, frequency), "characters")

    # Exercise 4
    sorted_x = sorted(frequency.items(), key=operator.itemgetter(1))
    exercise_4_first_letter = sorted_x.pop()[0]
    exercise_4_second_letter = sorted_x.pop()[0]

    print("\nExercise 4:")
    for filename in files:
        frequency_first, counter = exercise_4(filename)
        print("\tFile =", filename, "\tLetters:", frequency_first)

        print("\n\tSelected top used - starts with `" + exercise_4_first_letter + "` or `" + exercise_4_second_letter + "`")
        results = {exercise_4_first_letter: frequency_first.get(exercise_4_first_letter, {}), exercise_4_second_letter: frequency_first.get(exercise_4_second_letter, {})}
        for dictionary in results:
            for (key, value) in results.get(dictionary).items():
                if key != "total":
                    print("\t\t", dictionary + key, value / counter)
        print("\n\t------------------------------------------\n")

    # Exercise 5
    print("\nExercise 5:")
    filename = files[len(files) - 1]
    for i in [1, 3, 5]:
        print("Analyze file", filename)
        statistics = exercise_5_analyze(filename, i)
        print("Generate content")
        content = exercise_5_generator(statistics, i, 2_000_000)
        last_char = ""
        words = 0
        total_length = 0
        for char in content:
            if char != " ":
                total_length += 1
            if char == " " and last_char != " ":
                words += 1
            last_char = char

        print("Row =", i, "\tAverage length:", total_length / words)


if __name__ == "__main__":
    main()