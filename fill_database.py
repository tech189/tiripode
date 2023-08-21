import secret          # DB URL

import psycopg          # connect to database
import json             # open nominatives, stems, etc.

# TODO save DB_URL in a secrets file

connection_dict =  psycopg.conninfo.conninfo_to_dict(secret.DB_URI)

with open("generated-nominatives.json", "r") as nominatives_file, open("generated-stems.json", "r") as stems_file:
    nominatives_dict = json.load(nominatives_file)
    stems_dict = json.load(stems_file)

with psycopg.connect(**connection_dict) as conn:
    with conn.cursor() as cur:
        cur.execute("drop table nominatives")
        cur.execute("drop table stems")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS nominatives (
                id serial primary key,
                word varchar(50)
            )
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS stems (
                id serial primary key,
                word varchar(50)
            )
            """)
        # cur.execute("select * from nominatives")
        # cur.execute(
        #     "INSERT INTO nominatives (word) VALUES (%s)",
        #     ('hi',))
        cur.execute("select * from nominatives")
        print(cur.fetchall())
        
        cur.execute("select * from nominatives")
        print(cur.fetchall)
        
        for word in nominatives_dict:
            cur.execute(
                "INSERT INTO nominatives (word) VALUES (%s)",
                (word,)
            )
        for word in stems_dict:
            cur.execute(
                "INSERT INTO stems (word) VALUES (%s)",
                (word,)
            )

        


        # TODO is this last line necessary?
        conn.commit()