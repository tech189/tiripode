import json
from pathlib import Path

def print_first_decl_noun(noun):
    # TODO first decl masc!
    # TODO add allative?
    endings = {
        "singular": {
            # case: [syllabograms, pronunciation]
            "nominative": ["-a", "-ā̆"],
            "accusative": ["-a", "-ā̆n"],
            "genitive": ["-a", "-ās"],
            "dative": ["-a", "-āi"],
            "locative": ["-a", "-ai"], # Del Freo-Perna 2019 pronunciation is not certain for loc & ins
            "instrumental": ["-a", "-ā"] # Colvin the spelling does not allow us to say whether it was distinct in the singular.
        },
        "dual": {
            "nominative": ["-o", "-ō"],
            "accusative": ["-o", "-ō"],
            "genitive": ["-o-i", "-oi(h)i(n)"], # TODO check what the uppercase h means in Del Freo-Perna 2019
            "dative": ["-o-i", "-oi(h)i(n)"],
        },
        "plural": {
            "nominative": ["-a/-a3", "-ai"], # TODO check when a3 appears
            "accusative": ["-a", "-āns"],
            "genitive": ["-a-o", "-ā(h)ōn"],
            "dative/locative": ["-a-i", "-ā(h)i"],
            "instrumental": ["-a-pi", "-āp(h)i"]
        }
    }
    # print(type(endings["singular"]))
    for key, value in (endings["singular"]).items():
        print(noun + value[1])


def latin_to_linear_b(text):
    # split text by spaces and hyphens
    with open("sign-table.json", "r") as sign_file:
        sign_dict = json.load(sign_file)
    text = text.split("-")
    # print(text)
    output = ""
    for syllabogram in text:
        # print(sign_dict[syllabogram])
        if syllabogram in sign_dict:
            output = output + sign_dict[syllabogram]
    return output

def linear_b_to_latin(text):
    # split text by spaces and hyphens
    with open("sign-table.json", "r") as sign_file:
        sign_dict = json.load(sign_file)
    text = text.split("")
    print(text)
    output = ""
    for syllabogram in text:
        # print(sign_dict[syllabogram])
        if syllabogram in sign_dict.values():
            output = output + sign_dict[syllabogram]
    return output

print(latin_to_linear_b("ke-re-a2 *2̣0̣1̣VAS ti-ri-po-de  "))
# ,  a3-ke-u  ,  ke-re-si-jo  ,  we-ke   *201VAS   2   ti-ri-po  ,  e-me  ,  po-de  ,  o-wo-we   *201VAS   1   ti-ri-po  ,  ke-re-si-jo  ,  we-ke  ,  a-pu  ,  ke-ka-u-me-ṇọ[ qe-to     *203VAS   3   di-pa  ,  me-zo-e  ,  qe-to-ro-we   *202VAS   1   di-pa-e  ,  me-zo-e  ,  ti-ri-o-we-e    *202VAS    2   di-pa  ,  me-wi-jo  ,  qe-to-ro-we     *202VAS    1    di-pa  ,  me-wi-jo  ,  ti-ri-jo-we   *202VAS   1   di-pa  ,  me-wi-jo  ,  a-no-we   *202VAS   1"))
print(print_first_decl_noun("ko-to-na"))