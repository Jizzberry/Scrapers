import re

import requests
from bs4 import BeautifulSoup

from Utils import Constants
from Utils.DatabaseTools.db_tools_pornstars_list import add_items

starter = "A"
letter = "A"
blacklist = ["Special pages", "Boobpedia Copyright", "Privacy policy", "About Boobpedia", "Disclaimers", "Categories"]


def send_request(url):
    global letter, starter
    response = requests.post(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    f = soup.findAll("div", attrs={"class": "mw-category-group"})
    for link0 in f:
        g = link0.findAll("a", href=re.compile("/boobs/"), title=True)
        for i, link in enumerate(g):

            if i == (len(g) - 1):
                starter = link.text
                letter = starter[0]

            print(link.text)
            add_items(link.text, website=Constants.Type_Pornhub)


def populate_list():
    global letter, starter
    while letter != "Z":
        print("starter: "+starter)
        url = "http://www.boobpedia.com/wiki/index.php?title=Category:Porn_stars&pagefrom=" + starter + "#mw-pages"
        send_request(url)


