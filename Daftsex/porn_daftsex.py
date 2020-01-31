import random
import re

import requests
from bs4 import BeautifulSoup

from Utils import Constants


class QueryVideos:
    user_agent_list = Constants.user_agent_list

    def query(self, name):
        url = "https://daftsex.com/video/"
        name = re.split(' |-|_|[.,]', name)
        blacklist = Constants.blacklist

        for n in blacklist:
            if n in name:
                name.remove(n)

        for i, n in enumerate(name):
            if i < len(name):
                url = url + "%20" + n

        headers = {'User-Agent': random.choice(self.user_agent_list)}
        r = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        try:
            f = soup.find("div", attrs={'class': 'videos'}).findAll("div", attrs={'class': 'video-item'})
        except AttributeError:
            return None
        results = {}
        for item in f:
            link = "https://daftsex.com"+(item.find("a")['href'])
            title = item.find("a").find("div", attrs={'class': 'video-title'}).text
            results.update({link: {'title': title}})
        return results

    def scrape_video(self, url):
        return None

    def match_url(self, url):
        if len(re.findall("daftsex", url.lower())) > 0:
            return True
        else:
            return False

    def get_website_name(self):
        return "Daftsex"
