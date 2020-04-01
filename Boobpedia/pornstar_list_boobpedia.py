import re

import requests
from bs4 import BeautifulSoup

from Utils import Constants

starter = "A"
letter = "A"
blacklist = ["Special pages", "Boobpedia Copyright", "Privacy policy", "About Boobpedia", "Disclaimers", "Categories"]


def send_request(url):
    global letter, starter
    results_map = {}
    response = requests.post(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    f = soup.findAll("div", attrs={"class": "mw-category-group"})
    for link0 in f:
        g = link0.findAll("a", href=re.compile("/boobs/"), title=True)
        for i, link in enumerate(g):

            if i == (len(g) - 1):
                starter = link.text
                letter = starter[0]

            results_map.update({i: {
                'actress': link.text,
                'url_id': '',
                'website': Constants.Type_Pornhub
            }})
    return results_map


def populate_list():
    global letter, starter
    results_map = {}
    while letter != "Z":
        url = "http://www.boobpedia.com/wiki/index.php?title=Category:Porn_stars&pagefrom=" + starter + "#mw-pages"
        results_map.update(send_request(url))
    return results_map


