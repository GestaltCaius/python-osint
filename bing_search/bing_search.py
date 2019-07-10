import re

from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List
import requests

# Adding "real user" header in requests should prevent Bing from spotting us, allegedly.
headers_get = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}


@dataclass
class SearchResult:
    title: str = 'Untitled'
    url: str = 'No URL'
    caption: str = 'No caption'
    category: str = 'other'

    def domain(self) -> str:
        pattern = r'(http.?://)?(.*?)(/.*|$)'
        match = re.search(pattern, self.url)
        return match.group(2) if match else ''


    def __str__(self):
        return '[{}][{}] {} || {} (@ {})\n'.format(self.category.upper(), self.domain(), self.title, self.caption, self.url)


def bing_search(query: str) -> List[SearchResult]:
    """
    Gets bing search results as a list of SearchResult list
    :param query: bing search query, accepts "Google" Dorks
    :return: list of bing search results
    """
    session = requests.Session()
    url = 'http://www.bing.com/search?q={}&qs=n&form=QBRE&sp=-1'.format(query)
    response = session.get(url, headers=headers_get)
    soup = BeautifulSoup(response.text, "html.parser")

    output: List[SearchResult] = []
    results = soup.find_all('li', {'class': 'b_algo'})
    for result in results:
        title = result.find('h2').text.lower()
        url = result.find('div', {'class': 'b_attribution'}).text.lower()
        caption = result.find('p').text.lower()
        output.append(SearchResult(title=title, url=url, caption=caption))
    session.close()
    return output

