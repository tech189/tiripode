import secret          # DB URL
import log             # set up logging

import psycopg         # connect to database
import json            # return data as json
import argparse

connection_dict =  psycopg.conninfo.conninfo_to_dict(secret.DB_URI)

# get logger from main file
logger = log.logger

def get_database_size():
    with psycopg.connect(**connection_dict) as conn:
        with conn.cursor() as cur:

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

def parse(word):
    with psycopg.connect(**connection_dict) as conn:
        with conn.cursor() as cur:

            # cur.execute(
            #     "select entryid from dict_entry where word = %s::text",
            #     (word,)
            # )
            # entryid = cur.fetchone()[0]

            cur.execute("select dict_entry, formdeclension, formcase, formgender, formnumber, uncertaingender from inflection, form where inflection.form=form.formid and inflection = %s", (word,))
            output_dict = cur.fetchall()

            # result_dict = {}
            # for form in output_dict:
            #     print(list(form))
            #     print(form[0])
            #     form_list = list(form).remove(form[0])
            #     result_dict[form[0]] = form_list
            # print(result_dict)
    
    print(
        json.dumps(
            output_dict,
            indent=2, ensure_ascii=False
        )
    )

def lookup(entryid):
    with psycopg.connect(**connection_dict) as conn:
        with conn.cursor() as cur:

            cur.execute("select word, entrydefinition from dict_entry where entryid = %s", (entryid,))
            result = cur.fetchone()
            word = result[0]
            definition = result[1]

    
    print(
        json.dumps(
                {
                    "entry_id": int(entryid),
                    "word": word,
                    "definition": definition
                },
            indent=2, ensure_ascii=False
        )
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the Tiripode database for forms and lexicon entries")
    parser.add_argument("--parse", help="get a word parsed")
    # parser.add_argument("word", type=str, nargs=1, help="word to be parsed")
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