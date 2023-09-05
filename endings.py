endings = {
    "nouns": {
        # case: [syllabograms, pronunciation]
        # OR [[syllabograms 1, pronunciation 1], [syllabograms 2, pronunciation 2], ...]
        "1st declension": {
            "feminine": {
                "singular": {
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
                    "nominative": [["a", "ai"], ["a3", "ai"]],
                    "accusative": ["a", "āns"],
                    "allative": ["a-de", "ānsde"],
                    "genitive": ["a-o", "ā(h)ōn"],
                    "dative/locative": ["a-i", "ā(h)i"],
                    "instrumental": ["a-pi", "āp(h)i"]
                }
            },
            "masculine": {
                "singular": {
                    "nominative": ["a", "ā(s)"],
                    "genitive": ["a-o", "ā(h)o"]
                },
                "dual": {
                    "nominative": ["a-e", "ā(h)e"],
                    "accusative": ["a-e", "ā(h)e"]
                }
            }
        },
        "2nd declension": {
            "masculine": {
                "singular": {
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
                    "instrumental": [["o", "ōis"], ["o-pi", "o(i)p(h)i"]]
                }
            },
            "neuter": {
                "singular": {
                    "nominative": ["o", "on"]
                },
                "plural": {
                    "nominative": ["a", "a"],
                    "accusative": ["a", "a"]
                }
            }
        },
        "3rd declension": {
            "masculine/feminine": {
                "singular": {
                    "nominative": ["", ""],
                    "accusative": ["a", "a"],
                    "allative": ["a-de", "ade"],
                    "genitive": ["o", "os"],
                    "dative": [["e", "ei"], ["i", "i"]],
                    "locative": [["i", "i"], ["e", "ei"], ["e-u", "ēu"]],
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
            },
            "neuter": {
                "plural": {
                    "nominative": ["a", "a"],
                    "accusative": ["a", "a"]
                }
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
