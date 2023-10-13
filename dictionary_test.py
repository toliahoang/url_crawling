def letter_frequency(sentence):
    frequencies = {}
    for letter in sentence:
        frequency = frequencies.setdefault(letter, 0)
        print(frequency)
        frequencies[letter] = frequency + 1
    return frequencies




