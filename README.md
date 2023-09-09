# Tiripode
An online parser and grammar tool for Mycenaean Greek / Linear B

Running at: https://tech189.dev/tiripode

## Features
### Parse
- Works with 70% of 1st & 2nd declension nouns and adjectives
- Can enter in either Linear B syllabograms or transliterated (e.g. *wo-ko*)
- Gives root word, stem, part of speech, definition, possible forms
- Possible forms include declension, case, gender, number, ending pronunciation

### Dictionary
- Can look up any headword in the lexicon
- Can enter in either Linear B syllabograms or transliterated (e.g. *wo-ko*)

### Tables & Gloss
- To be built...
- (Tables work via CLI in `test.py`)

## Set up
Runs on a Raspberry Pi 3 with an NGINX webserver and PHP 7.4 already set up.
### Download source and prerequisites
Open a terminal window in your webserver home directory, then clone this repository:
```
git clone https://github.com/tech189/tiripode.git
```

Change directory:
```
cd tiripode
```

[Install `pyenv`](https://github.com/pyenv/pyenv#installation) if you don't already have it, then set up Python:
```
pyenv install 3.11.4
pyenv local 3.11.4
```

Create a virtual environment for Python and install the [required modules](/requirements.txt):
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Install PostgreSQL for the database and `libpq5` for `psycopg` to connect to it:
```
sudo apt install postgresql libpq5 -y
```

Set up a user for the database so you can connect as pi:
```
sudo su postgres
createuser pi -P --interactive
```

At the interactive prompt, choose
- no to "Shall the new role be a superuser?"
- yes to "Shall the new role be allowed to create databases?
- yes to "Shall the new role be allowed to create more new roles?"

Then type exit to leave PostgreSQL.

Create a `secret.py` file with your password from the previous step, for example:
```py
DB_URI = "postgres://pi:password@localhost/tiripode"
```

This will be used to connect to the database from Python.

Set up the database and create the tables:
```
psql postgres < setup_database.sql
```

Finally, generate the inflections and fill the database with them:
```
python3 prepare_data.py
python3 fill_database.py
```

Open the browser to `<your domain>/tiripode` to check it's all working!
