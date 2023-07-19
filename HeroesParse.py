import requests
import telebot
from bs4 import BeautifulSoup
import time
from requests_html import HTMLSession

heroes = requests.get("https://api.opendota.com/api/heroes").json()

with open ("heroes.txt", "w") as f:
    for i in range(len(heroes)):
        if i != len(heroes) - 1:
            f.write(f'{heroes[i]["id"]};{heroes[i]["localized_name"]}\n')
        else:
            f.write(f'{(heroes[i]["id"])};{heroes[i]["localized_name"]}')