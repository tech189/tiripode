import tools                # converting latin <-> linear b
import endings              # noun, verb endings
import log                  # set up logging

# get logger from main file
logger = log.logger

def check_ending(word, ending):
    if ending != "":
        # TODO Fix parsing of *56-ro2 - normalise a3 --> a???, ro2 --> ro?


        # scan ending, not just checking if it's in the word
        ending_pointer = len(ending) - 1
        word_pointer = len(word) - 1

        # logger.debug(f"\tending {ending[0]} word {word['transcription']}")
        # logger.debug(f"\tending pointer {ending_pointer} word pointer {word_pointer}")
        # logger.debug(f"\tending char {ending[0][ending_pointer]} word char {word['transcription'][word_pointer]}")

        while ending[ending_pointer] == word[word_pointer] and ending_pointer >= 0 and word_pointer >= 0:
            # logger.debug(f"loop\tending pointer {ending_pointer} word pointer {word_pointer}")
            # logger.debug(f"loop\tending char {ending[0][ending_pointer]} word char {word['transcription'][word_pointer]}")

            # endings match
            if ending_pointer == 0:
                return True
                # logger.debug(f'\t\t{declension} {case} {number} ({ending[0]})')
                forms += 1

                # if word["transcription"] not in possible_nouns.keys():
                #     possible_nouns[word["transcription"]] = []
                # possible_nouns[word["transcription"]].append(declension + " " + case + " " + number + " (" + ending[0] + ")")
            
            # decrement through both ending and word
            ending_pointer -= 1
            word_pointer -= 1

def parse(word):
    # TODO add short output option e.g. 3rd nom pl (e)
    
    counter = 0
    forms = 0
    possible_forms = []
    possible_stems = []

    # TODO stem should be generated from before this func
    word = tools.numeral_syllabograms_to_sound(word)["normalised"]

    # TODO determine case e.g. by participle me-no => 2nd
    # logger.debug(f"Parsing: {word}")
    for declension, number_set in endings.endings["nouns"].items():
        for gender, gender_set in number_set.items():
            for number, ending_set in gender_set.items():
                for case, ending_list in ending_set.items():
                    if isinstance(ending_list[0], list):
                        for ending in ending_list:
                            if check_ending(word, ending[0]):
                                stem = word[:-len(ending[0])]
                                if stem[-1] != "-":
                                    stem = stem + "-"

                                if stem not in possible_stems:
                                    possible_stems.append(stem)
                                
                                possible_forms.append({
                                    "declension": declension,
                                    "case": case,
                                    "gender": gender,
                                    "number": number,
                                    "ending": ending[0]
                                })

                    elif check_ending(word, ending_list[0]):
                        stem = word[:-len(ending_list[0])]
                        if stem[-1] != "-":
                            stem = stem + "-"

                        if stem not in possible_stems:
                            possible_stems.append(stem)
                        
                        possible_forms.append({
                            "declension": declension,
                            "case": case,
                            "gender": gender,
                            "number": number,
                            "ending": ending_list[0]
                        })
 
        # for key, value in third_decl.items():
        #     for case, ending in value.items():
        #         if ending[0] in word["transcription"][:-5]:
        #             print(word["transcription"] + " might be 3rd declension " + case + " " + key)
    counter += 1

    return {
        "possible_forms": possible_forms,
        "possible_stems": possible_stems
    }

if __name__ == "__main__":
    input_word = "ti-ri-po-de"
    # # input_word = "*34-ke-te-si"
    # # input_word = "*56-i-ti"
    # # input_word = '*56-ro2'
    # input_word = 'a-de-ra2'
    parses = parse(input_word)
    logger.info(f"Parsing: {input_word}")
    for form in parses["possible_forms"]:
        logger.info(f'\t\t{form["declension"]} {form["case"]} {form["gender"]} {form["number"]} ({form["ending"]})')
    logger.info(f'\tStem could be {", ".join(parses["possible_stems"])}')