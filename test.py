import json                  # importing sign table
import regex                 # splitting text into words
import unicodedata           # dealing with diacritics

# TODO move endings into json

def print_first_decl_noun(noun):
    # TODO first decl masc!
    # TODO add allative?
    endings = {
        "singular": {
            # case: [syllabograms, pronunciation]
            "nominative": ["a", "ā̆"],
            "accusative": ["a", "ā̆n"],
            "genitive": ["a", "ās"],
            "dative": ["a", "āi"],
            "locative": ["a", "ai"], # Del Freo-Perna 2019 pronunciation is not certain for loc & ins
            "instrumental": ["a", "ā"] # Colvin "the spelling does not allow us to say whether it was distinct in the singular."
        },
        "dual": {
            "nominative": ["o", "ō"],
            "accusative": ["o", "ō"],
            "genitive": ["o-i", "oi(h)i(n)"], # TODO check what the uppercase h means in Del Freo-Perna 2019
            "dative": ["o-i", "oi(h)i(n)"],
        },
        "plural": {
            "nominative": ["a/a3", "ai"], # TODO check when a3 appears
            "accusative": ["a", "āns"],
            "genitive": ["a-o", "ā(h)ōn"],
            "dative/locative": ["a-i", "ā(h)i"],
            "instrumental": ["a-pi", "āp(h)i"]
        }
    }

    print("First declension noun - " + noun + "\n")
    no_of_spaces = 16
    for key, value in endings.items():
        print(key.capitalize() + ":")
        for case, ending in value.items():
            spacer = ":" + " "  * (no_of_spaces - len(case))
            print(case + spacer + noun[:-1] + ending[0] + "  (-" + ending[1] + ")")
        print()

def print_second_decl_noun(noun):
    # TODO add second decl neuter
    # TODO add allative?
    endings = {
        "singular": {
            # case: [syllabograms, pronunciation]
            "nominative": ["o", "os"],
            "accusative": ["o", "on"],
            "genitive": ["o-jo", "oio"],
            "dative": ["o", "ōi"],
            "locative": ["o", "oi"],
            "instrumental": ["o", "ō"]
        },
        "dual": {
            "nominative": ["o", "ō"],
            "accusative": ["o", "ō"],
            "genitive": ["o-i", "oi(h)i(n)"], # TODO check what the uppercase h means in Del Freo-Perna 2019
            "dative": ["o-i", "oi(h)i(n)"],
        },
        "plural": {
            "nominative": ["o", "oi"],
            "accusative": ["o", "ons"],
            "genitive": ["o", "ōn"],
            "dative/locative": ["o-i", "oi(h)i"],
            "instrumental": ["o/o-pi", "ōis/o(i)p(h)i"]
        }
    }

    print("Second declension noun - " + noun + "\n")
    no_of_spaces = 16
    for key, value in endings.items():
        print(key.capitalize() + ":")
        for case, ending in value.items():
            spacer = ":" + " "  * (no_of_spaces - len(case))
            print(case + spacer + noun[:-1] + ending[0] + "  (-" + ending[1] + ")")
        print()

def print_third_decl_noun(noun, gen_sg):
    # TODO add third decl neuter
    # TODO add allative?
    endings = {
        "singular": {
            # case: [syllabograms, pronunciation]
            "nominative": ["", ""],
            "accusative": ["a", "a"],
            "genitive": ["o", "os"],
            "dative": ["e/i", "ei/i"],
            "locative": ["i/e/e-u", "i/ei/ēu"], # TODO double check this
            "instrumental": ["e", "ē"]
        },
        "dual": {
            "nominative": ["e", "e"],
            "accusative": ["e", "e"] # TODO no genitive/dative?
        },
        "plural": {
            "nominative": ["e", "es"],
            "accusative": ["a", "as"],
            "genitive": ["o", "ōn"],
            "dative/locative": ["si", "si"], # TODO which vowel to insert between gen sg stem and ending?
            "instrumental": ["pi", "p(h)i"]
        }
    }

    print("Third declension noun - " + noun + "\n")
    no_of_spaces = 16
    for key, value in endings.items():
        print(key.capitalize() + ":")
        for case, ending in value.items():
            spacer = ":" + " "  * (no_of_spaces - len(case))
            # special for third declension stems
            if case is "nominative" and key is "singular":
                print(case + spacer + noun + ending[0] + "  (-" + ending[1] + ")")
            else:
                print(case + spacer + gen_sg[:-1] + ending[0] + "  (-" + ending[1] + ")")
        print()

def print_verb(verb):
    # TODO add thematic verbs
    # TODO label verbs in lexicon as thematic/athematic, active/mediopassive
    endings = {
        "athematic": {
            "active": {
                "primary": { # TODO check if Colvin uses other word
                    # part: [syllabograms, pronunciation]
                    "3rd sg.": ["si", "si"],
                    "3rd pl.": ["si", "nsi"]
                },
                "secondary": {
                    "3rd sg.": ["", "/t"], # TODO check
                    "3rd pl.": ["", "/nt"] # TODO check
                }
            }
        }
        # TODO add mediopassive
    }

    print("Verb - " + verb + "\n")
    no_of_spaces = 16
    for key, value in endings["athematic"]["active"].items():
        print(key.capitalize() + ":")
        for case, ending in value.items():
            spacer = ":" + " "  * (no_of_spaces - len(case))
            print(case + spacer + verb + ending[0] + "  (-" + ending[1] + ")")
        print()

def latin_to_linear_b(text):
    # split text by spaces and hyphens
    with open("sign-table.json", "r") as sign_file:
        sign_dict = json.load(sign_file)
    # text = text.split()
    print(text)
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
    # TODO convert numerals!
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
        syllabograms = word.split("-")
        # print(syllabograms)
        for syllabogram in syllabograms:
            if syllabogram in sign_dict:
                output = output + sign_dict[syllabogram]
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

# print(latin_to_linear_b('''ke-re-a2 *2̣0̣1̣VAS ti-ri-po-de  ,  a3-ke-u  ,  ke-re-si-jo  ,  we-ke   *201VAS   2   ti-ri-po  ,  e-me  ,  po-de  ,  o-wo-we   *201VAS   1   ti-ri-po  ,  ke-re-si-jo  ,  we-ke  ,  a-pu  ,  ke-ka-u-me-ṇọ[ qe-to     *203VAS   3   di-pa  ,  me-zo-e  ,  qe-to-ro-we   *202VAS   1   di-pa-e  ,  me-zo-e  ,  ti-ri-o-we-e    *202VAS    2   di-pa  ,  me-wi-jo  ,  qe-to-ro-we     *202VAS    1    di-pa  ,  me-wi-jo  ,  ti-ri-jo-we   *202VAS   1   di-pa  ,  me-wi-jo  ,  a-no-we   *202VAS   1'''))

# print(linear_b_to_latin("𐀐𐀩𐀪𐀡"))

print_first_decl_noun("ko-to-na")
print_second_decl_noun("do-e-ro")
print_third_decl_noun("po-me", "po-me-no")
print_verb("pa")