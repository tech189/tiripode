import json                 # importing sign table
import regex                # splitting text into words
import unicodedata          # dealing with diacritics
import endings              # noun, verb endings
import logging              # TODO replace prints with logging debug/info

# TODO move endings into json

def print_first_decl_noun(noun):

    endings_dict = endings.endings["nouns"]["1st declension"]

    print("First declension noun - " + noun + "\n")
    no_of_spaces = 16
    for key, value in endings_dict.items():
        print(key.capitalize() + ":")
        for case, ending in value.items():
            spacer = ":" + " "  * (no_of_spaces - len(case))
            print(case + spacer + noun[:-1] + ending[0] + "  (-" + ending[1] + ")")
        print()

def print_second_decl_noun(noun):

    endings_dict = endings.endings["nouns"]["2nd declension"]

    print("Second declension noun - " + noun + "\n")
    no_of_spaces = 16
    for key, value in endings_dict.items():
        print(key.capitalize() + ":")
        for case, ending in value.items():
            spacer = ":" + " "  * (no_of_spaces - len(case))
            print(case + spacer + noun[:-1] + ending[0] + "  (-" + ending[1] + ")")
        print()

def print_third_decl_noun(noun, gen_sg):

    endings_dict = endings.endings["nouns"]["3rd declension"]

    print("Third declension noun - " + noun + "\n")
    no_of_spaces = 16
    for key, value in endings_dict.items():
        print(key.capitalize() + ":")
        for case, ending in value.items():
            spacer = ":" + " "  * (no_of_spaces - len(case))
            # special for third declension stems
            if case == "nominative" and key == "singular":
                print(case + spacer + noun + ending[0] + "  (-" + ending[1] + ")")
            else:
                print(case + spacer + gen_sg[:-1] + ending[0] + "  (-" + ending[1] + ")")
        print()

def print_verb(verb):
    
    endings_dict = endings.endings["verbs"]["athematic"]["active"]

    print("Verb - " + verb + "\n")
    no_of_spaces = 16
    for key, value in endings_dict.items():
        print(key.capitalize() + ":")
        for case, ending in value.items():
            spacer = ":" + " "  * (no_of_spaces - len(case))
            print(case + spacer + verb + ending[0] + "  (-" + ending[1] + ")")
        print()

def label_lexicon():
    with open("lexicon.json", "r") as sign_file:
        lexicon_dict = json.load(sign_file)
    
    # print(lexicon_dict[3]["transcription"])
    # prints "*34-ke-te-si"

    first_decl = endings.endings["nouns"]["1st declension"]
    second_decl = endings.endings["nouns"]["2nd declension"]
    third_decl = endings.endings["nouns"]["3rd declension"]
    active_verbs = endings.endings["verbs"]["athematic"]["active"]

    possible_nouns = {}

    counter = 0
    for word in lexicon_dict:
        if counter >= 0:
            # print("word:", word["transcription"])
            for declension, number_set in endings.endings["nouns"].items():
                for number, ending_set in number_set.items():
                    for case, ending in ending_set.items():
                        if ending[0] != "":
                            # scan ending, not just checking if it's in the word
                            ending_pointer = len(ending[0]) - 1
                            word_pointer = len(word["transcription"]) - 1

                            # print("\tending pointer", ending_pointer, "word pointer", word_pointer)
                            # print("\tending char",  ending[0][ending_pointer], "word char", word["transcription"][word_pointer])

                            while ending[0][ending_pointer] == word["transcription"][word_pointer] and ending_pointer >= 0 and word_pointer >= 0:
                                # print("\tending pointer", ending_pointer, "word pointer", word_pointer, "ending char",  ending[0][ending_pointer], "word char", word["transcription"][word_pointer])
                                if ending_pointer == 0:
                                    # print("\t", word["transcription"], "might be", declension, case, number, "(" + ending[0] + ")")
                                    if word["transcription"] not in possible_nouns.keys():
                                        possible_nouns[word["transcription"]] = []
                                    possible_nouns[word["transcription"]].append(declension + " " + case + " " + number + " (" + ending[0] + ")")
                                ending_pointer =- 1
                                word_pointer =- 1
                # for key, value in third_decl.items():
                #     for case, ending in value.items():
                #         if ending[0] in word["transcription"][:-5]:
                #             print(word["transcription"] + " might be 3rd declension " + case + " " + key)
            counter += 1
    
    with open("lexicon-labelled.json", "w") as labelled_file:
        labelled_file.write(json.dumps(possible_nouns, indent=2))
        
def label_lexicon2():
    with open("lexicon.json", "r") as sign_file:
        lexicon_dict = json.load(sign_file)
    
    labelled_dict = {}
    unlabelled_dict = {}
    counter = 0
    for word in lexicon_dict:
        if counter >= 0:
            search_list = ["anthroponym", "toponym"]
            if regex.search("(anthropo|topo|theo|ethno|patro|phyto)nym", word["definition"], regex.IGNORECASE):
                labelled_dict[word["transcription"]] = word
                labelled_dict[word["transcription"]]["category"] = "noun"
            else:
                unlabelled_dict[word["transcription"]] = word
            counter += 1
    
    with open("lexicon-labelled.json", "w") as labelled_file:
        labelled_file.write(json.dumps(labelled_dict, indent=2, ensure_ascii=False))
    with open("lexicon-unlabelled.json", "w") as labelled_file:
        labelled_file.write(json.dumps(unlabelled_dict, indent=2, ensure_ascii=False))

def fix_lexicon_transcriptions():
    with open("lexicon.json", "r") as sign_file:
        lexicon_dict = json.load(sign_file)
    
    for word in lexicon_dict:
        if word["word"] != latin_to_linear_b(word["transcription"], hyphens=True):
            print("word", word["word"], "transcription", word["transcription"], "--> fixed", latin_to_linear_b(word["transcription"], hyphens=True, debug=True))
        word["word"] = latin_to_linear_b(word["transcription"], hyphens=True)

def latin_to_linear_b(text, hyphens=False, debug=False):
    # split text by spaces and hyphens
    with open("sign-table.json", "r") as sign_file:
        sign_dict = json.load(sign_file)
    
    ids_dict = sign_dict["ids"]
    numeral_dict = sign_dict["numerals"]
    sign_dict = sign_dict["text"]
    # text = text.split()
    # print(text)
    # \pL = Letter (any)  \pM = Mark (any)
    text = filter(None, regex.split(r"([^\p{L}\p{M}0-9_\-\*])", text))
    # Print out the filtered text
    # for char in text:
    #     print("<" + char + ">")
    #     try:
    #         print([unicodedata.name(c) for c in char])
    #     except:
    #         print("can't find char name")
    output = ""
    # for word in text:
    #     word = word.split("-")
    # print(list(text))
    # TODO convert ideograms!
    for word in text:
        # print(sign_dict[syllabogram])
        # TODO if a word with funny characters then  normalise
        for char in word:
            if not unicodedata.is_normalized("NFD", char):
                print("<" + char + ">")
                char_parts = unicodedata.decomposition(char).split(" ")
                print(char_parts)
                for part in char_parts:
                    # first part will be normalised letter/number, second will be combining diacritic
                    escaped = "\\u" + part
                    print(escaped.encode().decode("unicode-escape"))
                    # this just prints, need to keep hold and recombine after conversion
        syllabograms = regex.split("(-)", word)
        if debug:
            print("debug")
            print(syllabograms)
        for syllabogram in syllabograms:
            if syllabogram.lower() in sign_dict:
                output = output + sign_dict[syllabogram.lower()]
            elif syllabogram.startswith("*"):
                try:
                    # search for number in syllabogram, ignores e.g. VAS
                    output = output + ids_dict[regex.search(r'\d+', syllabogram)[0]]
                except:
                    output = output + syllabogram
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
                        output = output + numeral_dict.get(str(ten_thousands), "") + numeral_dict.get(str(thousands), "") + numeral_dict.get(str(hundreds), "") + numeral_dict.get(str(tens), "") + numeral_dict.get(str(ones), "")
                except:
                    # couldn't convert numeral
                    output = output + syllabogram
            elif syllabogram == "-" and not hyphens:
                # don't add hyphens to output when not requested
                output = output
            else:
                output = output + syllabogram
    return output

def linear_b_to_latin(text):
    # split text by spaces and hyphens
    with open("sign-table.json", "r") as sign_file:
        sign_dict = json.load(sign_file)
    # text = text.split()
    # print(text)
    output = ""
    for syllabogram in text:
        # print(sign_dict[syllabogram])
        # if syllabogram in sign_dict.values():
        #     output = output + sign_dict[syllabogram]
        for key, value in sign_dict.items():
            if value == syllabogram:
                # print("key is", key, "value is", value)
                output = output + key + "-"
            elif output[:-1] == "-":
                output = output[-1:]
    return output

# PY Ta 641
print(latin_to_linear_b('''.1a                                                                                                                                                                                                                                                                               ,  ke-re-a2  , *2̣0̣1̣VAS[
.1b      ti-ri-po-de  ,  a3-ke-u  ,  ke-re-si-jo  ,  we-ke   *201VAS   2   ti-ri-po  ,  e-me  ,  po-de  ,  o-wo-we   *201VAS   1   ti-ri-po  ,  ke-re-si-jo  ,  we-ke  ,  a-pu  ,  ke-ka-u-me-ṇọ[
.2        qe-to     *203VAS   3   di-pa  ,  me-zo-e  ,  qe-to-ro-we   *202VAS   1   di-pa-e  ,  me-zo-e  ,  ti-ri-o-we-e    *202VAS    2   di-pa  ,  me-wi-jo  ,  qe-to-ro-we     *202VAS    1    [
.3        di-pa  ,  me-wi-jo  ,  ti-ri-jo-we   *202VAS   1   di-pa  ,  me-wi-jo  ,  a-no-we   *202VAS   1'''))

# print(linear_b_to_latin("𐀐𐀩𐀪𐀡"))

# TODO convert lexicon's words that have missing linear b signs like 'ai' and '*35'
# print(latin_to_linear_b("Po-ti-ni-a"))

# print_first_decl_noun("ko-to-na")
# print_second_decl_noun("do-e-ro")
# print_third_decl_noun("po-me", "po-me-no")
# print_verb("pa")
# label_lexicon()
# label_lexicon2()
fix_lexicon_transcriptions()