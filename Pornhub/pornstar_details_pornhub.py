import os
from urllib import request

import requests
from bs4 import BeautifulSoup, NavigableString

from Utils import Constants
from Utils.Configs.configParser import get_thumbnail_path
from Utils.DatabaseTools.db_tools_pornstar_details import add_items


class Pornstars:
    @staticmethod
    def get_name(soup):
        name = soup.find("h1", attrs={"itemprop": "name"})
        if name is None:
            name = soup.find("div", attrs={"class": "name"}).find("h1")
            if name is None:
                return None
            else:
                return name.text.strip()
        else:
            return name.text.strip()

    @staticmethod
    def get_birthdate(soup):
        birthdate = soup.find("span", attrs={"itemprop": "birthDate"})
        if birthdate is None:
            for info in soup.findAll("div", attrs={"class": "infoPiece"}):
                birthdate = info.find("span", string="Born:")
                if birthdate is not None:
                    text = [element for element in info if isinstance(element, NavigableString)]
                    return text[0].strip()
            if birthdate is None:
                return None
        else:
            return birthdate.text.strip()

    @staticmethod
    def get_birthplace(soup):
        birthplace = soup.find("span", attrs={"itemprop": "birthPlace"})
        if birthplace is None:
            for info in soup.findAll("div", attrs={"class": "infoPiece"}):
                birthplace = info.find("span", string="Birthplace:")
                if birthplace is not None:
                    text = [element for element in info if isinstance(element, NavigableString)]
                    return text[0].strip()
            if birthplace is None:
                return None
        else:
            return birthplace.text.strip()

    @staticmethod
    def get_height(soup):
        height = soup.find("span", attrs={"itemprop": "height"})
        if height is None:
            for info in soup.findAll("div", attrs={"class": "infoPiece"}):
                height = info.find("span", string="Height:")
                if height is not None:
                    text = [element for element in info if isinstance(element, NavigableString)]
                    return text[0].strip()
            if height is None:
                return None
        else:
            return height.text.strip()

    @staticmethod
    def get_weight(soup):
        weight = soup.find("span", attrs={"itemprop": "weight"})
        if weight is None:
            for info in soup.findAll("div", attrs={"class": "infoPiece"}):
                weight = info.find("span", string="Weight:")
                if weight is not None:
                    text = [element for element in info if isinstance(element, NavigableString)]
                    return text[0].strip()
            if weight is None:
                return None
        else:
            return weight.text.strip()

    @staticmethod
    def get_image(url, pid):
        r = requests.get(url=url)
        soup = BeautifulSoup(r.text, "html.parser")
        f = soup.find("div", attrs={'class': 'thumbImage'})
        if f is None:
            f = soup.find("div", attrs={'class': 'previewAvatarPicture'})
            if f is None:
                f = soup.find("div", attrs={'class': 'coverImage'})

        img_url = f.find("img")['src']
        k = open(os.path.join(get_thumbnail_path(), "p"+str(pid)+".png"), 'wb')
        k.write(request.urlopen(img_url).read())
        k.close()

        cover = soup.find("div", attrs={'class', "coverImage"})
        cover_url = cover.find("img")['src']
        k = open(os.path.join(get_thumbnail_path(), "p"+str(pid)+"-banner.png"), 'wb')
        k.write(request.urlopen(cover_url).read())
        k.close()

    def find_pornstar(self, name, pid, url_id):
        name = name.split(" ")
        if len(name) >= 2:
            url = "https://www.pornhub.org/pornstar/" + name[0] + "-" + name[1]
        else:
            url = "https://www.pornhub.org/pornstar/" + name[0]
        r = requests.get(url=url)
        soup = BeautifulSoup(r.text, "html.parser")
        # Keep this in different try since not all pages have a profile image
        try:
            self.get_image(url, pid)
        except AttributeError:
            pass

        try:
            name = self.get_name(soup)
            born = self.get_birthdate(soup)
            birthplace = self.get_birthplace(soup)
            height = self.get_height(soup)
            weight = self.get_weight(soup)

            return [name, born, birthplace, height, weight]

        except AttributeError as e:
            return None

    def fetch(self, scene_id, name, pid, url_id):
        data = self.find_pornstar(name, pid, url_id)
        if data is not None:
            if not data.count(None) == len(data):
                add_items(scene_id, data[0], data[1], data[2], data[3], data[4], pid)
                return True

    def get_website_name(self):
        return Constants.Type_Pornhub
