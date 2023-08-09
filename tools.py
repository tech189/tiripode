import log                  # set up logging

import json                 # importing sign table
import regex                # splitting text into words
import unicodedata          # dealing with diacritics

# get logger from main file
logger = log.logger

def latin_to_linear_b(text, hyphens=False, debug=False):
    # split text by spaces and hyphens
    with open("sign-table.json", "r") as sign_file:
        sign_dict = json.load(sign_file)
    
    ids_dict = sign_dict["ids"]
    numeral_dict = sign_dict["numerals"]
    sign_dict = sign_dict["text"]
    # logger.debug(text)
    # \pL = Letter (any)  \pM = Mark (any)
    text = filter(None, regex.split(r"([^\p{L}\p{M}0-9_\-\*])", text))
    # Print out the filtered text
    # for char in text:
    #     logger.debug(f"<{char}>")
    #     try:
    #         logger.debug([unicodedata.name(c) for c in char])
    #     except:
    #         logger.debug("can't find char name")
    output = ""
    # for word in text:
    #     word = word.split("-")
    # logger.debug(list(text))
    # TODO convert ideograms!
    for word in text:
        # logger.debug(sign_dict[syllabogram])
        # TODO if a word with funny characters then  normalise
        for char in word:
            if not unicodedata.is_normalized("NFD", char):
                logger.debug(f"<{char}>")
                char_parts = unicodedata.decomposition(char).split(" ")
                logger.debug(char_parts)
                for part in char_parts:
                    # first part will be normalised letter/number, second will be combining diacritic
                    escaped = "\\u" + part
                    logger.debug(escaped.encode().decode("unicode-escape"))
                    # this just prints, need to keep hold and recombine after conversion
        syllabograms = regex.split("(-)", word)
        if debug:
            logger.debug(syllabograms)
        for syllabogram in syllabograms:
            converted = ""
            if syllabogram.lower() in sign_dict:
                # output = output + sign_dict[syllabogram.lower()]
                converted = sign_dict[syllabogram.lower()]
            elif syllabogram.startswith("*"):
                try:
                    # search for number in syllabogram, ignores e.g. VAS
                    # output = output + ids_dict[regex.search(r'\d+', syllabogram)[0]]
                    converted = ids_dict[regex.search(r'\d+', syllabogram)[0]]
                except:
                    # output = output + syllabogram
                    converted = syllabogram
            elif syllabogram.isnumeric():
                try:
                    numeral = int(syllabogram)
                    # 99,999 is the maximum
                    if numeral < 100_000:
                        # get a list of each digit with leading zeroes
                        split_numeral = [int(digit) for digit in str(numeral).zfill(5)]
                        # assign each number
                        ten_thousands, thousands, hundreds, tens, ones = split_numeral[0] * 10_000, split_numeral[1] * 1_000, split_numeral[2] * 100, split_numeral[3] * 10, split_numeral[4]
                        # lookup each numeral and add to output
                        # output = output + numeral_dict.get(str(ten_thousands), "") + numeral_dict.get(str(thousands), "") + numeral_dict.get(str(hundreds), "") + numeral_dict.get(str(tens), "") + numeral_dict.get(str(ones), "")
                        converted = numeral_dict.get(str(ten_thousands), "") + numeral_dict.get(str(thousands), "") + numeral_dict.get(str(hundreds), "") + numeral_dict.get(str(tens), "") + numeral_dict.get(str(ones), "")
                except:
                    # couldn't convert numeral
                    # output = output + syllabogram
                    converted = syllabogram
            elif syllabogram == "-" and not hyphens:
                # don't add hyphens to output when not requested
                # output = output
                converted = converted
            else:
                # output = output + syllabogram
                converted = syllabogram
            logger.debug(f"{syllabogram} --> {converted}")
            output = output + converted
    return output

def linear_b_to_latin(text):
    # split text by spaces and hyphens
    with open("sign-table.json", "r") as sign_file:
        sign_dict = json.load(sign_file)
    text = filter(None, regex.split(r"([^\p{L}\p{M}0-9_\-\*])", text))
    
    output = ""
    # print out a list of words in the text - breaks the next part!
    # logger.debug(list(text))

    for word in text:
        # logger.debug("word: " + word)
        for char in word:
            converted = ""

            # try syllabic sounds
            for key, value in sign_dict["text"].items():
                if value == char:
                    converted = key + "-"
            
            # try chars by id
            if converted == "":
                for key, value in sign_dict["ids"].items():
                    if value == char:
                        converted = "*" + key
            
            # try aegean number
            if regex.search(r'[\U00010107-\U00010133]', word, regex.IGNORECASE):
                converted = 0
                for numeral in word:
                    for key, value in sign_dict["numerals"].items():
                        if value == numeral:
                            converted += int(key)
                converted = str(converted)

            # not in sign table so punctuation, keep
            if converted == "":
                converted = char

            if char != " ":
                logger.debug(f"{char} --> {converted}")
            output = output + converted

        # remove trailing -, e.g. di-pa-
        if output[-1:] == "-":
            output = output[:-1]
    return output