import tools                # converting latin <-> linear b
import prepare_data
import endings              # noun, verb endings
import log                  # set up logging

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

def main():
    logger.info("Printing out PY Ta 641:")
    PY_Ta_641 = '''.1a                                                                                                                                                                                                                                                                               ,  ke-re-a2  , *2̣0̣1̣VAS[
    .1b      ti-ri-po-de  ,  a3-ke-u  ,  ke-re-si-jo  ,  we-ke   *201VAS   2   ti-ri-po  ,  e-me  ,  po-de  ,  o-wo-we   *201VAS   1   ti-ri-po  ,  ke-re-si-jo  ,  we-ke  ,  a-pu  ,  ke-ka-u-me-ṇọ[
    .2        qe-to     *203VAS   3   di-pa  ,  me-zo-e  ,  qe-to-ro-we   *202VAS   1   di-pa-e  ,  me-zo-e  ,  ti-ri-o-we-e    *202VAS    2   di-pa  ,  me-wi-jo  ,  qe-to-ro-we     *202VAS    1    [
    .3        di-pa  ,  me-wi-jo  ,  ti-ri-jo-we   *202VAS   1   di-pa  ,  me-wi-jo  ,  a-no-we   *202VAS   1'''
    print(PY_Ta_641)
    logger.info("Converting PY Ta 641 to Linear B:")
    print(tools.latin_to_linear_b(PY_Ta_641))
    # TODO correct defect of *2̣0̣1̣VAS[ --> 2[ --> 𐀫[ --> ro[
    logger.info("Converting conversion of PY Ta 641 back to Latin letters:")
    print(tools.linear_b_to_latin(tools.latin_to_linear_b(PY_Ta_641)))

    logger.info("Converting 𐀐𐀩𐀪𐀡 to Latin letters:")
    print(tools.linear_b_to_latin("𐀐𐀩𐀪𐀡"))
    logger.info("Converting Po-ti-ni-a to Linear B:")
    print(tools.latin_to_linear_b("Po-ti-ni-a"))

    logger.info("Printing out 1st, 2nd, 3rd declensions and verbs:")
    print_first_decl_noun("ko-to-na")
    print_second_decl_noun("do-e-ro")
    print_third_decl_noun("po-me", "po-me-no")
    print_verb("pa")

    logger.info("Labelling the lexicon:")
    prepare_data.run()

if __name__ == "__main__":
    logger = log.logger
    main()