from datetime import datetime

from bs4 import BeautifulSoup
import json
import os
from os.path import dirname, join
import sys
import requests
from dotenv import load_dotenv
import psycopg2

ENVIRONMENT = sys.argv[1]

if ENVIRONMENT == 'local':
    app_dotenv_path = join(dirname(__file__), '', '../.environments/.local/.env')
    db_dotenv_path = join(dirname(__file__), '', '../.environments/.local/.postgres')
    DEBUG = True
else:
    DEBUG = False
    dotenv_path = join(dirname(__file__), '.environments/.production/.env')
load_dotenv(app_dotenv_path)
load_dotenv(db_dotenv_path)

ACCESS_KEY_FIXER = os.environ.get("ACCESS_KEY_FIXER")
URL_FIXER = os.environ.get("URL_FIXER")
HOME_URL = os.environ.get("HOME_URL")
TOKEN_BANXICO = os.environ.get("TOKEN_BANXICO")
URL_BANXICO = os.environ.get("URL_BANXICO")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
tmp_unavailable = 'Temporary Unavailable'
unavailable = {
    'last_updated': tmp_unavailable,
    'time_registered': tmp_unavailable,
    'value': tmp_unavailable,
    'service': tmp_unavailable
}


def db_handler(prices):
    conn = psycopg2.connect(host='postgres',
                            port=POSTGRES_PORT,
                            user=POSTGRES_USER,
                            password=POSTGRES_PASSWORD,
                            database=POSTGRES_DB)
    cursor = conn.cursor()
    sql_str = 'INSERT INTO price (last_updated, time_registered, value, service) VALUES(%s, %s, %s, %s)'
    for price in prices:
        cursor.execute(sql_str, (price['last_updated'], price['time_registered'], price['value'], price['service']))
        print('Register query')
    conn.commit()
    cursor.close()
    conn.close()


def get_price_fixer():
    try:
        querystring = {
            "access_key": ACCESS_KEY_FIXER,
            "symbols": "USD,AUD,CAD,PLN,MXN",
            "format": "1"
        }
        response = requests.request("GET", URL_FIXER, params=querystring)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            last_updated = datetime.strptime(json_data['date'], '%Y-%m-%d')
            value = json_data['rates']['MXN']
            now = datetime.now().isoformat()
            return {
                'last_updated': last_updated.isoformat(),
                'value': float(value),
                'service': 'fixer',
                'time_registered': now
            }
        else:
            return unavailable
    except ValueError as ve:
        print(ve)
        return unavailable
    else:
        return unavailable


def get_price_banxico():
    try:
        querystring = {"token": TOKEN_BANXICO}
        response = requests.get(URL_BANXICO, params=querystring)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            array_price_date = json_data['bmx']['series'][0]['datos'][-1]
            date_price = array_price_date['fecha']
            last_updated = datetime.strptime(date_price, '%d/%m/%Y')
            value = array_price_date['dato']
            now = datetime.now().isoformat()
            return {
                'last_updated': last_updated.isoformat(),
                'value': float(value),
                'service': 'banxico',
                'time_registered': now
            }
        else:
            return unavailable
    except ValueError as ve:
        print(ve)
        return unavailable
    else:
        return unavailable


def get_price_scrape():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            s = BeautifulSoup(response.text, 'lxml')
            date_price_scraped = s.find('td', attrs={'style': "padding-top:5px;padding-bottom:5px;"})
            price_scraped = s.find('tr', attrs={'class': 'renglonNon'}).findAll('td')

            # in this part the text is formatted to obtain the price only
            date_price = " ".join(date_price_scraped.contents[0].text.split())
            last_updated = datetime.strptime(date_price, '%d/%m/%Y')
            price_string = ''.join(price_scraped[3].contents[0].splitlines()).split()[0]
            now = datetime.now().isoformat()
            return {
                'last_updated': last_updated.isoformat(),
                'value': float(price_string),
                'service': 'federation',
                'time_registered': now
            }
        else:
            return unavailable
    except ValueError as ve:
        print(ve)
        return unavailable


if __name__ == '__main__':
    db_handler([get_price_fixer(), get_price_banxico(), get_price_scrape()])
