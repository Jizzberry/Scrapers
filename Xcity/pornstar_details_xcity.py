import os
from urllib import request

import requests
from bs4 import BeautifulSoup

from Utils.Configs.configParser import get_thumbnail_path
from Utils.DatabaseTools.db_tools_pornstar_details import add_items


class Pornstars():

    def get_details(self, soup):
        f = soup.find("dl", attrs={"class": "profile"}).findAll("dd")
        dob, height, size, birthplace, name = "", "", "", "", ""
        name = soup.find("div", attrs={'class': "itemBox"}).find("h1").text
        for item in f:
            if item.find("span").text == "Date of birth":
                dob = item.text
            elif item.find("span").text == "Height":
                height = item.text
            elif item.find("span").text == "Size":
                size = item.text
            elif item.find("span").text == "City of Born":
                birthplace = item.text

        return name, dob, height, size, birthplace

    def get_image(self, soup, pid):
        f = soup.find("img", attrs={'class': 'actressThumb'})
        img_url = "https:" + f['src']
        k = open(os.path.join(get_thumbnail_path(), "p"+str(pid)+".png"), 'wb')
        k.write(request.urlopen(img_url).read())
        k.close()

    def find_pornstar(self, name, pid, url_id):

        url = "https://xxx.xcity.jp/idol/detail/" + str(url_id)
        r = requests.get(url=url)
        soup = BeautifulSoup(r.text, "html.parser")

        try:
            name, born, height, weight, birthplace = self.get_details(soup)
            self.get_image(soup, pid)

            return [name, born, birthplace, height, weight]

        except AttributeError as e:
            return None

    def fetch(self, scene_id, name, pid, url_id):
        data = self.find_pornstar(name, pid, url_id)
        if data is not None:
            if not data.count(None) == len(data):
                add_items(scene_id, data[0], data[1], data[2], data[3], data[4], pid)