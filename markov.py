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

def split_spaces_and_keep_punctuation(string, punctuation):
    words = []
    word  = ""
    
    for char in string:
        
        if char in " \n":
            if word != "": words.append(word)
            word = ""
            continue

        if char in punctuation:
            if word != "": words.append(word)
            words.append(char)
            word = ""
            continue

        word += char

    return words

def tokenize(string, specials, punctuation):
    for special, to_replace in specials.items():
        string = string.replace(special, to_replace)
        
    return split_spaces_and_keep_punctuation(
        cap_repetitions((''.join(string)).lower(), 5).strip(),
        punctuation
    )

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

def generate(data, punctuation):
    prefix_list = list(data.keys())
    begin       = choice(prefix_list)

    suffix_list = list(data[begin].keys())
    after       = choices(suffix_list, weights = [data[begin][key] for key in suffix_list])[0]
    
    sentence = begin + (" " if after not in punctuation else "") + after

    while after in data:
        begin = after

        suffix_list = list(data[begin].keys())
        after       = choices(suffix_list, weights = [data[begin][key] for key in suffix_list])[0]

        sentence += (" " if after not in punctuation else "") + after

    return sentence
