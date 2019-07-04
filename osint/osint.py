from typing import List

from bing_search.bing_search import SearchResult, bing_search
from osint import constants


class Osint:
    results: List[SearchResult]

    def __init__(self, username: str, email: str, firstname: str, lastname: str):
        self.results = []
        self.username = username.lower()
        self.email = email.lower()
        self.firstname = firstname.lower()
        self.lastname = lastname.lower()

    def search(self) -> List[SearchResult]:
        """
        OSINT search by username, email and/or real name
        :return: list of search results
        """
        for site in constants.websites:
            if self.username:
                self.results += bing_search('"{}" site:{}'.format(self.username, site))
            if self.email:
                self.results += bing_search('"{}" site:{}'.format(self.email, site))
            if self.firstname and self.lastname:
                self.results += bing_search('"{}" site:{}'.format(self.firstname + " " + self.lastname, site))

        self.remove_irrelevant_results()
        return self.results

    def remove_irrelevant_results(self):
        is_relevant = lambda result: self.username in result.title \
                                     or self.username in result.caption \
                                     or self.email in result.title \
                                     or self.email in result.caption \
                                     or self.firstname + " " + self.lastname in result.title \
                                     or self.firstname + " " + self.lastname in result.caption

        self.results = list(filter(is_relevant, self.results))

