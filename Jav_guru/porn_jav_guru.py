import random
import re

import requests
from bs4 import BeautifulSoup

from Utils import Constants


class QueryVideos:
    user_agent_list = Constants.user_agent_list

    def query(self, query):
        url = "https://jav.guru/?s="+query.replace(" ", "+")
        headers = {'User-Agent': random.choice(self.user_agent_list)}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        noresults = soup.find("div", attrs={'class': 'no-result'})
        if noresults is None:
            f = soup.find("div", attrs={'class': 'content csearch'}) \
                .findAll("div", attrs={'class': "result-item"})
            links = {}
            for item in f:
                data = item.find("div", attrs={"class": 'title'}).find("a")
                links.update({
                    data['href']: {
                        'title': data.text,
                    }
                })
            return links
        else:
            return None

    def scrape_video(self, url):
        headers = {'User-Agent': random.choice(self.user_agent_list)}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        meta = soup.findAll("div", attrs={'class': "meta"})
        name_list = []
        category_list = []
        for data in meta:
            post2 = data.find("div", attrs={'class': 'post2'})
            tag_url = post2.findAll("a")
            for url in tag_url:
                url_split = url['href'].split("/")
                for item in url_split:
                    if item == "tag":
                        category_list.append(url.text)
            actressTag = data.findAll("p")
            for actress in actressTag:
                f = actress.find("strong")
                if f:
                    if f.text == 'Actress: ':
                        actressA = actress.findAll("a", attrs={'rel': 'tag'}, recursive=False)
                        for name in actressA:
                            name_list.append(name.text)

        title = soup.find("h2", attrs={'class': 'titl'}).text  # Not a typo
        return [name_list, title, category_list]

    def match_url(self, url):
        if len(re.findall("jav.guru", url.lower())) > 0:
            return True
        else:
            return False

    def get_website_name(self):
        return "Daftsex"