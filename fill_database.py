import secret          # DB URL
import endings         # generate forms table
import log             # set up logging

import psycopg         # connect to database
import json            # open nominatives, stems, etc.
from tqdm import tqdm  # progress bar

connection_dict =  psycopg.conninfo.conninfo_to_dict(secret.DB_URI)

# get logger from main file
logger = log.logger

def run():
    with open("lexicon.json", "r") as lexicon_file, open("generated-inflections.json", "r") as inflections_file:
        lexicon_dict = json.load(lexicon_file)
        inflections_dict = json.load(inflections_file)

    decl = endings.endings["nouns"]
    decl.pop("3rd declension")

    with psycopg.connect(**connection_dict) as conn:
        with conn.cursor() as cur:

            # check tables are empty
            cur.execute("select count(*) from dict_entry")
            dict_entry_count = cur.fetchone()[0]
            if dict_entry_count != 0:
                logger.error("Database has already been filled! Run 'psql postgres < setup_database.sql' before running this.")
                exit()

            # fill table dict_entry
            logger.info("Filling table dict_entry with words from lexicon...")
            for _, word in tqdm(lexicon_dict.items()):

                stems = word.get("stems", None)
                if stems is not None:
                    stems = ",".join(stems)

                cur.execute(
                    "INSERT INTO dict_entry (word, entrydefinition, category, stem) VALUES (%s, %s, %s, %s)",
                    (word["transcription"], word["definition"], word.get("category", None), stems)
                )
            
            # fill table form
            logger.info("Filling table form with endings...")
            for declension, decl_set in tqdm(decl.items()):
                for gender, gender_set in decl_set.items():
                    for number, ending_set in gender_set.items():
                        for case, ending in ending_set.items():
                            if isinstance(ending[0], list):
                                for end in ending:
                                    # logger.debug(declension, case, gender, number, end[0])
                                    cur.execute(
                                        "INSERT INTO form (formdeclension, formcase, formgender, formnumber, formending, formpronunciation) VALUES (%s, %s, %s, %s, %s, %s)",
                                        (declension, case, gender, number, end[0], end[1])
                                    )
                            else:
                                # logger.debug(declension, case, gender, number, ending[0])
                                cur.execute(
                                    "INSERT INTO form (formdeclension, formcase, formgender, formnumber, formending, formpronunciation) VALUES (%s, %s, %s, %s, %s, %s)",
                                    (declension, case, gender, number, ending[0], ending[1])
                                )

            # fill table inflection
            logger.info("Filling table inflection with generated inflections...")
            for word, inflection_set in tqdm(inflections_dict.items()):
                for inflection, possible_forms in inflection_set.items():
                    for form in possible_forms:

                        gender_uncertain = False

                        if "*" in form["gender"]:
                            form["gender"] = form["gender"].replace("*", "")
                            gender_uncertain = True


                        cur.execute(
                            "select formid from form where formdeclension = %s and formcase = %s and formgender = %s and formnumber = %s and formending = %s",
                            (form["declension"], form["case"], form["gender"], form["number"], form["ending"])
                        )

                        formid = cur.fetchone()[0]
                        
                        # # debug:
                        # try:
                        #     formid = cur.fetchone()[0]
                        # except:
                        #     formid = None
                        # if formid == None:
                        #     print((form["declension"], form["case"], form["gender"], form["number"], form["ending"]))


                        cur.execute(
                            "select entryid from dict_entry where word = %s::text",
                            (word,)
                        )

                        entryid = cur.fetchone()[0]

                        # # debug
                        # try:
                        #     entryid = cur.fetchone()[0]
                        # except:
                        #     entryid = None
                        # if entryid == None:
                        #     print(inflection)

                        cur.execute(
                            "INSERT INTO inflection (inflection, form, dict_entry, uncertaingender) VALUES (%s, %s, %s, %s)",
                            (inflection, formid, entryid, gender_uncertain)
                        )

            # cur.execute("select stem from dict_entry where entryid < 50 and stem is not null")
            # logger.debug(cur.fetchall())
            
            # cur.execute("select formid from form where formdeclension = '2nd declension' and formcase = 'instrumental' and formgender = 'masculine' and formnumber = 'plural' and formending = 'o-pi'")
            # logger.debug(cur.fetchone()[0])

            # TODO do a join with form to check an inflection
            # select * from inflection where inflectionid = 1 join with form via formid????

            cur.execute("select count(*) from dict_entry")
            dict_entry_count = cur.fetchone()[0]

            cur.execute("select count(*) from form")
            form_count = cur.fetchone()[0]

            cur.execute("select count(*) from inflection")
            inflection_count = cur.fetchone()[0]


            # TODO is this last line necessary?
            conn.commit()

    logger.info(f"Filled the database with {dict_entry_count} dictionary entries, {form_count} forms, and {inflection_count} inflections.")

if __name__ == "__main__":
    run()