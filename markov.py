from random import choice, choices

def cap_repetitions(string, length):
    new_string     = ""
    repeated_chars = ""
    quantity       = length

    for char in string:
        if char in repeated_chars:
            quantity -= 1
        else:
            repeated_chars = ""
            quantity       = length

        if quantity > 0:
            new_string += char

        repeated_chars += char

    return new_string

def tokenize(string, specials = {"-": " ", "@": " "}):
    for special, to_replace in specials.items():
        string = string.replace(special, to_replace)
        
    return cap_repetitions((''.join(string)).lower(), 5).strip().split()

def self_pairs(tokens, default = ""):
    return list(zip(tokens, tokens[1:])) if len(tokens) > 1 else [(default, tokens[0])]

def learn(tokens, __data = {}):
    data = __data

    for prefix, suffix in self_pairs(tokens):
        if prefix not in data:
            data[prefix] = {}

        if suffix not in data[prefix]:
            data[prefix][suffix] = 0

        data[prefix][suffix] += 0.1

    return data

def generate(data):
    prefix_list = list(data.keys())
    begin       = choice(prefix_list)

    suffix_list = list(data[begin].keys())
    after       = choices(suffix_list, weights = [data[begin][key] for key in suffix_list])[0]

    sentence = begin + " " + after

    while after in data:
        begin = after

        suffix_list = list(data[begin].keys())
        after       = choices(suffix_list, weights = [data[begin][key] for key in suffix_list])[0]

        sentence += " " + after

    return sentence
