import secret          # DB URL
import log             # set up logging
import tools           # conversions of characters

import psycopg         # connect to database
import json            # return data as json
import argparse        # cli argument parsing
import regex           # check for linear b text

# get postgres connection parameters from secret file
connection_dict =  psycopg.conninfo.conninfo_to_dict(secret.DB_URI)

# get logger from main file
logger = log.logger

def get_database_size():
    try:
        with psycopg.connect(**connection_dict) as conn:
            with conn.cursor() as cur:

                # count length of each table
                cur.execute("select count(*) from dict_entry")
                dict_entry_count = cur.fetchone()[0]
                
                cur.execute("select count(*) from form")
                form_count = cur.fetchone()[0]

                cur.execute("select count(*) from inflection")
                inflection_count = cur.fetchone()[0]
        
        print(
            json.dumps(
                {
                    "lexicon_size": dict_entry_count,
                    "form_count": form_count,
                    "inflection_count": inflection_count
                },
                indent=2, ensure_ascii=False
            )
        )
    except Exception as e:
        print(
            json.dumps(
                    {
                        "error": "Could not get database size",
                        "exception": str(e)
                    },
                indent=2, ensure_ascii=False
            )
        )

def parse(word):
    try:
        if regex.search(r'[\U00010000-\U000100FA]', word, regex.IGNORECASE):
            # linear b characters found, convert to transliteration
            word = tools.linear_b_to_latin(word)
            
        with psycopg.connect(**connection_dict) as conn:
            with conn.cursor() as cur:

                # look up in a join of the inflection table and the form table
                cur.execute("select dict_entry, formdeclension, formcase, formgender, formnumber, uncertaingender, formpronunciation from inflection, form where inflection.form=form.formid and inflection = %s", (word,))
                output_dict = cur.fetchall()

                # # debug:
                # result_dict = {}
                # for form in output_dict:
                #     print(list(form))
                #     print(form[0])
                #     form_list = list(form).remove(form[0])
                #     result_dict[form[0]] = form_list
                # print(result_dict)

        if len(output_dict) != 0:
            # as long as there are results
            print(
                json.dumps(
                    output_dict,
                    indent=2, ensure_ascii=False
                )
            )
        else:
            print(
                json.dumps(
                    {
                        "error": "Word not found"
                    },
                    indent=2, ensure_ascii=False
                )
            )
    except Exception as e:
        print(
            json.dumps(
                    {
                        "error": "Couldn't parse word",
                        "exception": str(e)
                    },
                indent=2, ensure_ascii=False
            )
        )

def lookup(entry):
    try:
        # user can give either entryid or just the word, need to convert if number
        try:
            entry = int(entry)
        except:
            entry = str(entry)

        with psycopg.connect(**connection_dict) as conn:
            with conn.cursor() as cur:
            
                # user enters an entryid
                if isinstance(entry, int):
                    cur.execute("select word, entrydefinition, category, stem from dict_entry where entryid = %s", (entry,))
                    result = cur.fetchone()
                    word = result[0]
                    definition = result[1]
                    category = result[2]
                    stem = result[3]
                
                # user enters a word
                elif isinstance(entry, str):
                    if regex.search(r'[\U00010000-\U000100FA]', entry, regex.IGNORECASE):
                        # linear b characters found, convert to transliteration
                        entry = tools.linear_b_to_latin(entry)
                    cur.execute("select entryid, word, entrydefinition, category, stem from dict_entry where word = %s", (entry,))
                    result = cur.fetchone()
                    entry = result[0]
                    word = result[1]
                    definition = result[2]
                    category = result[3]
                    stem = result[4]

        print(
            json.dumps(
                # TODO check if this if statement is redundant
                    {
                        "entry_id": int(entry),
                        "word": word,
                        "definition": definition,
                        "category": category,
                        "stem": stem
                    } if isinstance(entry, int) else 
                    {
                        "entry_id": entry,
                        "word": word,
                        "definition": definition,
                        "category": category,
                        "stem": stem
                    },
                indent=2, ensure_ascii=False
            )
        )
    except Exception as e:
        import traceback
        print(
            json.dumps(
                    {
                        "error": "Word not found",
                        "exception": traceback.format_tb(e.__traceback__)
                    },
                indent=2, ensure_ascii=False
            )
        )

if __name__ == "__main__":
    # get cli arguments to pick function to run
    parser = argparse.ArgumentParser(description="Query the Tiripode database for forms and lexicon entries")
    parser.add_argument("--parse", help="get a word parsed")
    parser.add_argument("--lookup", help="get a dictionary entry")
    parser.add_argument("--size", help="get number of entries in database", action="store_true")
    parser.add_argument("--debug", help="print detailed info for debugging", action="store_true")
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(log.logging.DEBUG)
    
    if args.size:
        get_database_size()
    elif args.parse:
        parse(args.parse)
    elif args.lookup:
        lookup(args.lookup)