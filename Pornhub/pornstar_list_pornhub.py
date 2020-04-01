import requests
from bs4 import BeautifulSoup

from Utils import Constants

last_page = 1364


def send_request(url):
    response = requests.post(url=url)
    results_map = {}
    soup = BeautifulSoup(response.text, "html.parser")
    f = soup.findAll("a", attrs={"class": "js-mxp",
                                 "data-mxptype": "Pornstar"})

    for i, link in enumerate(f):
        print(link['data-mxptext'])
        results_map.update({i: {
            'actress': link['data-mxptext'].strip(),
            'url_id': '',
            'website': Constants.Type_xcity
        }})
    return results_map

def populate_list():
    results_map = {}
    page = 1
    while page < last_page:
        url = "https://www.pornhub.com/pornstars?o=t&page=" + str(page)
        results_map.update(send_request(url))
        page += 1
    return results_map
