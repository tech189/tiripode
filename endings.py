endings = {
    "nouns": {
        "1st declension": {
            # TODO first decl masc!
            "singular": {
                # case: [syllabograms, pronunciation]
                "nominative": ["a", "ā̆"],
                "accusative": ["a", "ā̆n"],
                "allative": ["a-de", "ā̆n-de"],
                "genitive": ["a", "ās"],
                "dative": ["a", "āi"],
                # Del Freo-Perna 2019 pronunciation is not certain for loc & ins
                "locative": ["a", "ai"],
                # Colvin "the spelling does not allow us to say whether it was distinct in the singular."
                "instrumental": ["a", "ā"]
            },
            "dual": {
                "nominative": ["o", "ō"],
                "accusative": ["o", "ō"],
                # TODO check what the uppercase h means in Del Freo-Perna 2019
                "genitive": ["o-i", "oi(h)i(n)"],
                "dative": ["o-i", "oi(h)i(n)"],
            },
            "plural": {
                "nominative": ["a/a3", "ai"],  # TODO check when a3 appears
                "accusative": ["a", "āns"],
                "allative": ["a-de", "ānsde"],
                "genitive": ["a-o", "ā(h)ōn"],
                "dative/locative": ["a-i", "ā(h)i"],
                "instrumental": ["a-pi", "āp(h)i"]
            }
        },
        "2nd declension": {
            # TODO add second decl neuter
            "singular": {
                # case: [syllabograms, pronunciation]
                "nominative": ["o", "os"],
                "accusative": ["o", "on"],
                "allative": ["o-de", "onde"],
                "genitive": ["o-jo", "oio"],
                "dative": ["o", "ōi"],
                "locative": ["o", "oi"],
                "instrumental": ["o", "ō"]
            },
            "dual": {
                "nominative": ["o", "ō"],
                "accusative": ["o", "ō"],
                # TODO check what the uppercase h means in Del Freo-Perna 2019
                "genitive": ["o-i", "oi(h)i(n)"],
                "dative": ["o-i", "oi(h)i(n)"],
            },
            "plural": {
                "nominative": ["o", "oi"],
                "accusative": ["o", "ons"],
                "allative": ["o-de", "o(n)sde"],
                "genitive": ["o", "ōn"],
                "dative/locative": ["o-i", "oi(h)i"],
                "instrumental": ["o/o-pi", "ōis/o(i)p(h)i"]
            }
        },
        "3rd declension": {
            # TODO add third decl neuter
            "singular": {
                # case: [syllabograms, pronunciation]
                "nominative": ["", ""],
                "accusative": ["a", "a"],
                "allative": ["a-de", "ade"],
                "genitive": ["o", "os"],
                "dative": ["e/i", "ei/i"],
                "locative": ["i/e/e-u", "i/ei/ēu"],  # TODO double check this
                "instrumental": ["e", "ē"]
            },
            "dual": {
                "nominative": ["e", "e"],
                "accusative": ["e", "e"]  # TODO no genitive/dative?
            },
            "plural": {
                "nominative": ["e", "es"],
                "accusative": ["a", "as"],
                "allative": ["a-de", "asde"],
                "genitive": ["o", "ōn"],
                # TODO which vowel to insert between gen sg stem and ending?
                "dative/locative": ["si", "si"],
                "instrumental": ["pi", "p(h)i"]
            }
        }
    },
    "verbs": {
        # TODO add thematic verbs
        # TODO label verbs in lexicon as thematic/athematic, active/mediopassive
        "athematic": {
            "active": {
                "primary": {  # TODO check if Colvin uses other word
                    # part: [syllabograms, pronunciation]
                    "3rd sg.": ["si", "si"],
                    "3rd pl.": ["si", "nsi"]
                },
                "secondary": {
                    "3rd sg.": ["", "/t"],  # TODO check
                    "3rd pl.": ["", "/nt"]  # TODO check
                }
            }
        }
        # TODO add mediopassive
    }
}
