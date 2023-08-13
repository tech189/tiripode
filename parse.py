import tools                # converting latin <-> linear b
import endings              # noun, verb endings
import log                  # set up logging

import json                 # importing sign table

# get logger from main file
logger = log.logger

def parse(word):
    with open("lexicon.json", "r") as lexicon_file:
        lexicon_dict = json.load(lexicon_file)
    
    counter = 0
    forms = 0
    possible_stems = []
    # TODO determine case e.g. by participle me-no => 2nd
    logger.info(f"Parsing: {word}")
    for declension, number_set in endings.endings["nouns"].items():
        for number, ending_set in number_set.items():
            for case, ending in ending_set.items():
                # only look at words labelled as nouns & adjectives
                if ending[0] != "":
                    # scan ending, not just checking if it's in the word
                    ending_pointer = len(ending[0]) - 1
                    word_pointer = len(word) - 1

                    # logger.debug(f"\tending {ending[0]} word {word['transcription']}")
                    # logger.debug(f"\tending pointer {ending_pointer} word pointer {word_pointer}")
                    # logger.debug(f"\tending char {ending[0][ending_pointer]} word char {word['transcription'][word_pointer]}")

                    while ending[0][ending_pointer] == word[word_pointer] and ending_pointer >= 0 and word_pointer >= 0:
                        # logger.debug(f"loop\tending pointer {ending_pointer} word pointer {word_pointer}")
                        # logger.debug(f"loop\tending char {ending[0][ending_pointer]} word char {word['transcription'][word_pointer]}")

                        # endings match
                        if ending_pointer == 0:
                            stem = word[:-len(ending[0])] + "-"
                            if stem not in possible_stems:
                                possible_stems.append(stem)
                            logger.info(f'\t\t{declension} {case} {number} ({ending[0]})')
                            forms += 1
                            # if word["transcription"] not in possible_nouns.keys():
                            #     possible_nouns[word["transcription"]] = []
                            # possible_nouns[word["transcription"]].append(declension + " " + case + " " + number + " (" + ending[0] + ")")
                        
                        # decrement through both ending and word
                        ending_pointer -= 1
                        word_pointer -= 1
        # for key, value in third_decl.items():
        #     for case, ending in value.items():
        #         if ending[0] in word["transcription"][:-5]:
        #             print(word["transcription"] + " might be 3rd declension " + case + " " + key)
    counter += 1
    logger.info(f'\tStem could be {", ".join(possible_stems)}')

if __name__ == "__main__":
    parse("ti-ri-po-de")