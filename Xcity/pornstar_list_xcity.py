import requests
from bs4 import BeautifulSoup

from Utils import Constants


def send_request(url, total_count):
    response = requests.post(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    f = soup.find("div", attrs={"id": "avidol"}).findAll("div", attrs={'class': 'itemBox'})
    results_map = {}
    for i, item in enumerate(f):
        box = item.find("a")
        actress = box['title']
        url_id = box['href'].split("/")[1]
        results_map.update({total_count: {
            'actress':actress,
            'url_id': url_id,
            'website': Constants.Type_xcity
        }})
        total_count += 1
    return total_count, results_map


def get_pageno(url):
    response = requests.post(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    f = soup.find("div", attrs={"id": "avidol"}).find("ul", attrs={'class': 'pageScrl'}).findAll("li")
    return f[len(f) - 2].text


def populate_list():
    results_map = {}
    search_sequence = {"あ": ["あ", "い", "う", "え", "お"],
                       "か": ["か", "き", "く", "け", "こ"],
                       "さ": ["さ", "し", "す", "せ", "そ"],
                       "た": ["た", "ち", "つ", "て", "と"],
                       "な": ["な", "に", "ぬ", "ね", "の"],
                       "は": ["は", "ひ", "ふ", "へ", "ほ"],
                       "ま": ["ま", "み", "む", "め", "も"],
                       "や": ["や", "ゆ", "よ"],
                       "ら": ["ら", "り", "る", "れ", "ろ"],
                       "わ": ["わ"]
                       }
    total_count = 0
    for key, value in search_sequence.items():
        for item in value:
            url = "https://xxx.xcity.jp/idol/?kana=" + key + "&ini=" + item + "&num=90"
            page_no = get_pageno(url)

            for i in range(1, int(page_no)):
                url = "https://xxx.xcity.jp/idol/?kana=" + key + "&ini=" + item + "&num=90&page=" + str(i)
                total_count, rmap = (send_request(url, total_count))
                results_map.update(rmap)
    return results_map

