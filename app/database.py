import os
import sys
from os.path import join, dirname
import psycopg2
from dotenv import load_dotenv

ENVIRONMENT = 'local'

if ENVIRONMENT == 'local':
    app_dotenv_path = join(dirname(__file__), '', '../.environments/.local/.env')
    db_dotenv_path = join(dirname(__file__), '', '../.environments/.local/.postgres')
    DEBUG = True
else:
    DEBUG = False
    dotenv_path = join(dirname(__file__), '.environments/.production/.env')
load_dotenv(app_dotenv_path)
load_dotenv(db_dotenv_path)

POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")


def db_handler_query():
    conn = psycopg2.connect(host='localhost',
                            port=POSTGRES_PORT,
                            user=POSTGRES_USER,
                            password=POSTGRES_PASSWORD,
                            database=POSTGRES_DB)
    cursor = conn.cursor()
    sql_str = "SELECT * FROM price ORDER BY time_registered DESC LIMIT 6"
    cursor.execute(sql_str)
    rows = cursor.fetchall()
    results = []
    for row in rows:
        results.append(row)
    cursor.close()
    conn.close()
    return results


if __name__ == '__main__':
    db_handler()
