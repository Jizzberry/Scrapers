import requests
from bs4 import BeautifulSoup

from .. import Constants
from ..DatabaseTools.db_tools_pornstars_list import add_items

last_page = 1364


def send_request(url):
    response = requests.post(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    f = soup.findAll("a", attrs={"class": "js-mxp",
                                 "data-mxptype": "Pornstar"})

    for link in f:
        print(link['data-mxptext'])
        add_items(link['data-mxptext'].strip(), website=Constants.Type_Pornhub)


def populate_list():
    page = 1
    while page < last_page:
        url = "https://www.pornhub.com/pornstars?o=t&page=" + str(page)
        send_request(url)
        page += 1
