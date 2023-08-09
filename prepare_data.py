import tools                # converting latin <-> linear b
import endings              # noun, verb endings
import log                  # set up logging

import json                 # importing sign table
import regex                # splitting text into words

# get logger from main file
logger = log.logger

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
        # logger.debug("word: " + word["transcription"])
        for declension, number_set in endings.endings["nouns"].items():
            for number, ending_set in number_set.items():
                for case, ending in ending_set.items():
                    if ending[0] != "":
                        # scan ending, not just checking if it's in the word
                        ending_pointer = len(ending[0]) - 1
                        word_pointer = len(word["transcription"]) - 1

                        # logger.debug("\tending pointer " + ending_pointer + " word pointer " + word_pointer)
                        # logger.debug("\tending char " + ending[0][ending_pointer] + " word char " + word["transcription"][word_pointer])

                        while ending[0][ending_pointer] == word["transcription"][word_pointer] and ending_pointer >= 0 and word_pointer >= 0:
                            # logger.debug("\tending pointer " + ending_pointer + " word pointer " + word_pointer)
                            # logger.debug("\tending char " + ending[0][ending_pointer] + " word char " + word["transcription"][word_pointer])
                            if ending_pointer == 0:
                                logger.debug(f'\t {word["transcription"]} might be {declension} {case} {number} ({ending[0]})')
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
    
    with open("lexicon-possible-forms.json", "w") as labelled_file:
        labelled_file.write(json.dumps(possible_nouns, indent=2))
    
    logger.info(f"Labelled {counter} words.")
        
def label_lexicon2():
    with open("lexicon.json", "r") as sign_file:
        lexicon_dict = json.load(sign_file)
    
    labelled_dict = {}
    unlabelled_dict = {}
    labelled_counter = 0
    unlabelled_counter = 0
    for word in lexicon_dict:
        if regex.search("(anthropo|topo|theo|ethno|patro|phyto)nym", word["definition"], regex.IGNORECASE):
            labelled_dict[word["transcription"]] = word
            labelled_dict[word["transcription"]]["category"] = "noun"
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
    
    with open("lexicon-original.json", "r") as sign_file:
        lexicon_dict = json.load(sign_file)
    
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

def run():
    fix_lexicon_transcriptions() # lexicon-original.json --> lexicon.json
    label_lexicon() # lexicon.json --> lexicon-possible-forms.json
    label_lexicon2() # lexicon.json --> lexicon-labelled.json, lexicon-unlabelled.json

if __name__ == "__main__":
    run()