""" ========
::: Imports.
======== """

from random import choice, choices
from json   import loads, dumps
from re     import sub

""" ====================
::: Namespacing classes.
==================== """

class Punctuations:
    default = ".,:;!?"

class Filters:
    hyper_links = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    
    default = [ (hyper_links, "") ]

class String: # Just for reading purposes
    empty = ""
    space = " "

""" ==================
::: Lexical Functions.
================== """

def limit_repetitions(string: str, max_repetitions: int) -> str:
    string_prime   = ""
    repeated_chars = ""
    quantity       = max_repetitions

    for char in string:
        if char in repeated_chars:
            quantity -= 1
        else:
            repeated_chars = ""
            quantity       = max_repetitions

        if quantity > 0:
            string_prime += char

        repeated_chars += char

    return string_prime

def filter_patterns(string: str, filters: list[tuple[str, str]]):
    for (pattern, to_replace) in filters:
        string = sub(pattern, to_replace, string)

    return string

def clean(string: str, max_repetitions: int, filters: list[tuple[str, str]]) -> str:
    return limit_repetitions(
        filter_patterns
        (
            string.lower(), filters
        ).strip(), max_repetitions
    )

def tokenize(string: str, punctuations: str, max_repetitions: int, filters: list[tuple[str, str]]):
    words = []
    word  = ""
    
    string = clean(string, max_repetitions, filters)

    for char in string:
        
        if char in " \n":
            if word is not String.empty: words.append(word)
            
            word = ""
            continue

        if char in punctuations:
            if word is not String.empty: words.append(word)
            
            words.append(char)
            
            word = ""
            continue

        word += char

    if word is not String.empty: words.append(word)

    return words

def look_ahead_pairs(tokens: list[str], begin_default = "") -> list[(str, str)] | None:
    lt = len(tokens)
    
    if lt == 0: return None
    if lt >  1: return list( zip(tokens, tokens[ 1 : ]) )

    return [ (begin_default, tokens[0]) ]

""" ===============
::: Helper classes.
=============== """

class JFile:
    @staticmethod
    def try_load_set_default(file_name: str) -> dict | None:
        try: return JFile.load(file_name)
        
        except FileNotFoundError:
            print(f"File \"{file_name}\" not found: Creating a default with same name.")
            JFile.save(file_name, {})

            return None

    @staticmethod
    def load(file_name: str) -> dict:
        with open(file_name, 'r') as file:
            return loads(''.join(file.readlines()))

    @staticmethod
    def save(file_name: str, data: dict) -> None:
        with open(file_name, 'w+') as file:
            file.write(dumps(data, indent = 4))

""" ========================
::: The Markov chains class.
======================== """

class Chains:
    def __init__(self, max_recursion: int, char_limit: int, punctuations: str, filters: list[tuple[str, str]], words: dict[str, dict[str, float]] = { }, file_name: str = ""):
        self.max_recursion = max_recursion
        self.char_limit    = char_limit
        self.punctuations  = punctuations
        self.filters       = filters
        self.words         = words
        self.file_name     = file_name

        if self.file_name is not String.empty:
            if (data := JFile.try_load_set_default(self.file_name)):
                self.words |= data

    def save(self):
        if self.file_name is not String.empty:
            JFile.save(self.file_name, self.words)
            return

        print("Please create a Markov instance with a file_name, if you wish to save.")

    def feed(self, string: str) -> bool:
        tokens = tokenize(string, self.punctuations, 5, self.filters)
        pairs  = look_ahead_pairs(tokens)

        if pairs:
            for prefix, suffix in pairs:
                if prefix not in self.words:
                    self.words[prefix] = {}

                if suffix not in self.words[prefix]:
                    self.words[prefix][suffix] = 0

                self.words[prefix][suffix] += 1

            return True

        return False

    def generate(self, bias: str = None):

        if bias and bias in self.words:
            first = bias
        else:
            prefix_list = list(
                filter(
                    lambda word: word not in self.punctuations, self.words.keys()
                )
            )
            first = choice( prefix_list )
        
        selected = self.words[first]

        suffix_list    = list(selected.keys())
        suffix_weights = list(selected.values())

        after = choices(
            suffix_list,
            suffix_weights
        )[0]

        sentence = first + (
            String.space if after not in self.punctuations else String.empty
        ) + after

        recursion_level = 0

        while after in self.words:
            first     = after
            last_word = after

            selected = self.words[first]

            suffix_list    = list(selected.keys())
            suffix_weights = list(selected.values())

            after = choices(
                suffix_list,
                suffix_weights
            )[0]

            sentence += (
                String.space if after not in self.punctuations else String.empty
            ) + after

            if after is last_word:
                if (recursion_level := recursion_level + 1) > self.max_recursion:
                    break
            else:
                recursion_level = 0

        return sentence [ : self.char_limit ]
