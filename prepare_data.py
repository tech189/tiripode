import tools                # converting latin <-> linear b
import endings              # noun, verb endings
import log                  # set up logging
import parse                # get parses

import json                 # importing sign table
import regex                # splitting text into words
from nltk import pos_tag, word_tokenize

# get logger from main file
logger = log.logger

# TODO save and load lexicon functions

def label_possible_forms():
    with open("lexicon.json", "r") as lexicon_file:
        lexicon_dict = json.load(lexicon_file)
    
    # print(lexicon_dict[3]["transcription"])
    # prints "*34-ke-te-si"

    first_decl = endings.endings["nouns"]["1st declension"]
    second_decl = endings.endings["nouns"]["2nd declension"]
    third_decl = endings.endings["nouns"]["3rd declension"]
    active_verbs = endings.endings["verbs"]["athematic"]["active"]

    possible_nouns = {}

    counter = 0
    forms = 0
    # TODO determine case e.g. by participle me-no => 2nd
    for _, word in lexicon_dict.items():
        # logger.debug("word: " + word["transcription"])
        for declension, number_set in endings.endings["nouns"].items():
            for number, ending_set in number_set.items():
                for case, ending in ending_set.items():
                    # only look at words labelled as nouns & adjectives
                    if ending[0] != "" and word.get("category", "") in ["noun", "adjective"]:
                        # scan ending, not just checking if it's in the word
                        ending_pointer = len(ending[0]) - 1
                        word_pointer = len(word["transcription"]) - 1

                        # logger.debug(f"\tending {ending[0]} word {word['transcription']}")
                        # logger.debug(f"\tending pointer {ending_pointer} word pointer {word_pointer}")
                        # logger.debug(f"\tending char {ending[0][ending_pointer]} word char {word['transcription'][word_pointer]}")

                        while ending[0][ending_pointer] == word["transcription"][word_pointer] and ending_pointer >= 0 and word_pointer >= 0:
                            # logger.debug(f"loop\tending pointer {ending_pointer} word pointer {word_pointer}")
                            # logger.debug(f"loop\tending char {ending[0][ending_pointer]} word char {word['transcription'][word_pointer]}")

                            # endings match
                            if ending_pointer == 0:
                                logger.debug(f'\t {word["transcription"]} might be {declension} {case} {number} ({ending[0]})')
                                forms += 1
                                if word["transcription"] not in possible_nouns.keys():
                                    possible_nouns[word["transcription"]] = []
                                possible_nouns[word["transcription"]].append(declension + " " + case + " " + number + " (" + ending[0] + ")")
                            
                            # decrement through both ending and word
                            ending_pointer -= 1
                            word_pointer -= 1
            # for key, value in third_decl.items():
            #     for case, ending in value.items():
            #         if ending[0] in word["transcription"][:-5]:
            #             print(word["transcription"] + " might be 3rd declension " + case + " " + key)
        counter += 1
    
    with open("lexicon-possible-forms.json", "w") as labelled_file:
        labelled_file.write(json.dumps(possible_nouns, indent=2))
    
    logger.info(f"Labelled {counter} words with {forms} possible forms.")
        
def label_lexicon():
    with open("lexicon.json", "r") as lexicon_file:
        lexicon_dict = json.load(lexicon_file)
    
    labelled_dict = {}
    unlabelled_dict = {}
    labelled_counter = 0
    unlabelled_counter = 0
    for word in lexicon_dict:
        if regex.search("(anthropo|topo|theo|ethno|patro|phyto)nym", word["definition"], regex.IGNORECASE):
            labelled_dict[word["transcription"]] = word
            labelled_dict[word["transcription"]]["category"] = "noun"
            labelled_counter += 1
        elif regex.search("adjective", word["definition"], regex.IGNORECASE):
            labelled_dict[word["transcription"]] = word
            labelled_dict[word["transcription"]]["category"] = "adjective"
            labelled_counter += 1
        else:
            unlabelled_dict[word["transcription"]] = word
            unlabelled_counter += 1
    
    with open("lexicon-labelled.json", "w") as labelled_file:
        labelled_file.write(json.dumps(labelled_dict, indent=2, ensure_ascii=False))
    with open("lexicon-unlabelled.json", "w") as labelled_file:
        labelled_file.write(json.dumps(unlabelled_dict, indent=2, ensure_ascii=False))
    
    logger.info(f"Labelled {labelled_counter} words but left {unlabelled_counter} unlabelled.")

def fix_lexicon_transcriptions():
    # fixes transcriptions which have latin letters in, doesn't fix removed signs such as *35 - see Del Freo-Perna 2019 pg. 131
    
    with open("lexicon-original.json", "r") as lexicon_file:
        lexicon_dict = json.load(lexicon_file)
    
    counter = 0

    for word in lexicon_dict:
        # fix ai --> a3
        if "ai" in word["word"].split("-"):
            logger.debug("fixing " + word["word"] + " --> " + word["transcription"].replace("ai", "a3"))
            word["transcription"] = word["transcription"].replace("ai", "a3")
        
        # run each transcription through tools.latin_to_linear_b()
        if word["word"] != tools.latin_to_linear_b(word["transcription"], hyphens=True):
            logger.debug("word " + word["word"] + " transcription " + word["transcription"] + " --> fixed " + tools.latin_to_linear_b(word["transcription"], hyphens=True, debug=True))
            word["word"] = tools.latin_to_linear_b(word["transcription"], hyphens=True)
            counter += 1
    
    with open("lexicon.json", "w") as labelled_file:
        labelled_file.write(json.dumps(lexicon_dict, indent=2, ensure_ascii=False))
    
    logger.info(f"Fixed {counter} transcription errors.")

def combine_lexicons():
    with open("lexicon-labelled.json", "r")  as labelled_file, open("lexicon-unlabelled.json", "r") as unlabelled_file:
        labelled_dict = json.load(labelled_file)
        unlabelled_dict = json.load(unlabelled_file)
    
    combined_dict = labelled_dict | unlabelled_dict

    with open("lexicon.json", "w") as combined_file:
        combined_file.write(json.dumps(combined_dict, indent=2, ensure_ascii=False))
    
    logger.info(f"Combined the labelled and unlabelled lexicons.")

def label_short_definitions():
    with open("lexicon.json", "r") as lexicon_file:
        lexicon_dict = json.load(lexicon_file)
    
    try:
        pos_tag(word_tokenize("test"))
    except:
        import nltk
        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")
        # for getting noun phrases - too hard
        # nltk.download("maxent_ne_chunker")
        # nltk.download("words")

    short_defs = 0
    untagged = 0
    for _, word in lexicon_dict.items():
        if len(word["definition"].split()) == 1:
            pos = pos_tag(word_tokenize(word["definition"]))
            # logger.debug(f'word {word["definition"]} is probably a {pos[0][1]}')

            # nouns, plurals, proper names
            if pos[0][1] in ["NN", "NNS", "NNP"]:
                lexicon_dict[word["transcription"]]["category"] = "noun"
                short_defs += 1
            # adjectives, verb past participles
            elif pos[0][1] in ["JJ", "VBN"]:
                lexicon_dict[word["transcription"]]["category"] = "adjective"
                short_defs += 1
            # else:
            #     logger.debug(f'word {word["definition"]} is probably a {pos[0][1]}')

        elif len(word["definition"].split()) < 10:
            # TODO use POS tagging to extract noun phrases to e.g. categorise nouns - too hard
            # logger.debug(f'word {word["transcription"]} means {word["definition"]}')
            # pos = pos_tag(word_tokenize("It means " + word["definition"] + "."))
            # entities = chunk.ne_chunk(pos)
            # logger.debug(entities)
            untagged += 1
    
    with open("lexicon.json", "w") as lexicon_file:
        lexicon_file.write(json.dumps(lexicon_dict, indent=2, ensure_ascii=False))
    
    logger.info(f"Labelled {short_defs} short definitions and left {untagged} untagged.")

def generate_nominative_list():
    with open("lexicon.json", "r") as lexicon_file:
        lexicon_dict = json.load(lexicon_file)
    
    nominatives = []
    stems = []
    for _, word in lexicon_dict.items():
        if word["transcription"] == 'ti-ri-po-de':
            egg = 1
        if word.get("category", "") == "noun" or word.get("category", "") == "adjective":
            parses = parse.parse(word["transcription"])

            print(parses["possible_stems"])
            if '--' in parses["possible_stems"][0]:
                egg = 1

            for form in parses["possible_forms"]:
                if "nominative" in form["case"] and "singular" in form["number"]:
                    nominatives.append(word["transcription"])
                    if parses["possible_stems"] not in stems:
                        stems += parses["possible_stems"]
    
    with open("generated-nominatives.json", "w") as nominative_file:
        nominative_file.write(json.dumps(nominatives, indent=2, ensure_ascii=False))
    with open("generated-stems.json", "w") as stem_file:
        stem_file.write(json.dumps(stems, indent=2, ensure_ascii=False))
    
    logger.info(f"Generated a list of {len(nominatives)} nominative singular dictionary headwords and their stems.")

def generate_inflected_list():
    with open("generated-nominatives.json", "r") as lexicon_file:
        lexicon_dict = json.load(lexicon_file)
    
    inflections = []
    for _, word in lexicon_dict.items():
        if word.get("category", "") == "noun" or word.get("category", "") == "adjective":
            parses = parse.parse(word["transcription"])

            for form in parses["possible_forms"]:
                if "nominative" in form["case"] and "singular" in form["number"]:
                    inflections.append(word["transcription"])
    
    with open("generated-stems.json", "w") as stem_file:
        stem_file.write(json.dumps(inflections, indent=2, ensure_ascii=False))
    
    logger.info(f"Generated a list of {len(inflections)} inflections from the nominative singular dictionary headwords.")


def count_labelled():
    with open("lexicon.json", "r") as lexicon_file:
        lexicon_dict = json.load(lexicon_file)
    
    count_labelled = 0
    for _, word in lexicon_dict.items():
        if word.get("category", "") != "":
            count_labelled += 1
    
    count_total = len(lexicon_dict)
    count_percentage = count_labelled/count_total * 100
    
    logger.info(f"There are {count_labelled}/{count_total} words ({count_percentage:.1f}%) categorised in the lexicon.")

def run():
    fix_lexicon_transcriptions() # lexicon-original.json --> lexicon.json
    label_lexicon() # lexicon.json --> lexicon-(un)labelled.json
    combine_lexicons() # lexicon-(un)labelled.json --> lexicon.json
    label_short_definitions() # lexicon.json --> lexicon.json
    # label_possible_forms() # lexicon.json --> lexicon-possible-forms.json
    count_labelled()
    generate_nominative_list() # lexicon.json --> generated-nominatives.json


if __name__ == "__main__":
    run()