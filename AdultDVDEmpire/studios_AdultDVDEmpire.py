import requests
from bs4 import BeautifulSoup


class Studios:
    def fetch_studios(self):
        url = 'https://www.adultdvdempire.com/all-porn-movie-studios.html'
        r = requests.get(url=url)
        soup = BeautifulSoup(r.text, "html.parser")
        f = soup.find("div", attrs={'class': 'row spacing-bottom'}).findAll("a",
                                                                            attrs={'category': 'All Studio Page - DVD'}
                                                                            )
        studios = []
        for studio in f:
            studios.append(studio.text)

        return studios
