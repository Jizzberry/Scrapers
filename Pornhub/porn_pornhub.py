import random
import re

import requests
from bs4 import BeautifulSoup

from Utils import Constants


class QueryVideos:
    user_agent_list = Constants.user_agent_list

    def query(self, query):
        url = "https://www.pornhub.org/video/search?search="+query.replace(" ", "+").replace("[", "").replace("]", "")
        headers = {'User-Agent': random.choice(self.user_agent_list)}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        noresults = soup.find("div", attrs={'class': 'noResultsWrapper'})
        if noresults is None:
            f = soup.find("ul", attrs={'id': 'videoSearchResult'}) \
                .findAll("a", attrs={'class': "linkVideoThumb js-linkVideoThumb img"})
            links = {}
            for link in f:
                links.update({
                    "https://pornhub.org"+link['href']: {
                        'title': link['title'],
                    }
                })
            return links
        else:
            return None

    def scrape_video(self, url):
        headers = {'User-Agent': random.choice(self.user_agent_list)}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        pornstar_name = soup.findAll("div", attrs={'class': "video-info-row"})
        name_list = []
        for names in pornstar_name:
            wrapper = names.find("div", attrs={'class': "pornstarsWrapper"})
            if wrapper is not None:
                for name in wrapper.findAll("a", attrs={'class': 'pstar-list-btn js-mxp'}):
                    name_list.append(name['data-mxptext'])

        title = soup.find("div", attrs={'class': 'title-container'}).find("span").text
        categories = soup.find("div", attrs={'class': 'categoriesWrapper'}).findAll("a")
        category_list = []
        for category in categories:
            category_list.append(category.text)
        return [name_list, title, category_list]

    def match_url(self, url):
        if len(re.findall("pornhub", url.lower())) > 0:
            return True
        else:
            return False

    def get_website_name(self):
        return "Pornhub"