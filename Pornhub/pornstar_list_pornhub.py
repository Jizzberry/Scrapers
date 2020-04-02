import requests
from bs4 import BeautifulSoup

from Utils import Constants

last_page = 1364


def send_request(url, total_count):
    response = requests.post(url=url)
    results_map = {}
    soup = BeautifulSoup(response.text, "html.parser")
    f = soup.findAll("a", attrs={"class": "title js-mxp",
                                 "data-mxptype": "Pornstar"})

    for i, link in enumerate(f):
        results_map.update({total_count: {
            'actress': link['data-mxptext'].strip(),
            'url_id': '',
            'website': Constants.Type_Pornhub
        }})
        total_count += 1

    return total_count, results_map


def populate_list():
    results_map = {}
    page = 1
    total_count = 0
    while page < last_page:
        url = "https://www.pornhub.com/pornstars?o=t&page=" + str(page)
        total_count, rmap = send_request(url, total_count)
        results_map.update(rmap)
        page += 1
        print(results_map)
    return results_map

populate_list()
