from bing_search.bing_search import SearchResult, bing_search
from osint import constants
from pathlib import Path
from typing import List

import logging
import os
import re

filepath = os.path.join(Path.cwd(), 'osint_result.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s',
    filename=filepath,
    filemode='w' #clear everytime
)
logger = logging.getLogger(__name__)


class Osint:
    results: List[SearchResult]

    def __init__(self, username: str, email: str, firstname: str, lastname: str):
        self.results = []
        self.username = username.lower() if username else None
        self.email = email.lower() if email else None
        self.firstname = firstname.lower() if firstname else None
        self.lastname = lastname.lower() if lastname else None

    def search(self) -> List[SearchResult]:
        """
        OSINT search by username, email and/or real name
        :return: list of search results
        """
        for site in constants.websites:
            if self.username:
                results = bing_search('"{}" site:{}'.format(self.username, site))
                results = self.map_result_category(results, 'username')
                self.results += results

            if self.email:
                results = bing_search('"{}" site:{}'.format(self.email, site))
                results = self.map_result_category(results, 'email')
                self.results += results

            if self.firstname and self.lastname:
                results = bing_search('"{}" site:{}'.format(self.firstname + " " + self.lastname, site))
                results += bing_search('"{}" site:{}'.format(self.lastname + " " + self.firstname, site))

                results = self.map_result_category(results, 'real name')
                self.results += results

        self.remove_irrelevant_results()

        if self.username:
            for site in constants.social_websites:
                results = bing_search('"{}" -site:{}/{} site:{}'.format(self.username, site, self.username, site))
                results = self.map_result_category(results, 'social media')
                self.results += results

        if self.email:
            pattern = r'.*@(.*)'
            match = re.search(pattern, self.email)
            domain = match.group(1) if match else ''
            results = bing_search('"{}" site:{} filecategory:csv | filecategory:xls | filecategory:xlsx'.format(self.email, domain))
            results = self.map_result_category(results, 'mailing list file')
            self.results += results
        
        if self.firstname and self.lastname:
            results = bing_search('"CV" OR "Curriculum Vitae" filetype:PDF "{}" "{}"'.format(self.firstname, self.lastname))
            results = self.map_result_category(results, 'CV')
            self.results += results


    def remove_irrelevant_results(self):
        is_relevant = lambda result: (self.username and (self.username in result.title \
                                      or self.username in result.caption)) \
                                     or (self.email and (self.email in result.title \
                                         or self.email in result.caption)) \
                                     or (self.firstname and (self.lastname and \
                                         self.firstname + " " + self.lastname in result.title \
                                         or self.firstname + " " + self.lastname in result.caption))

        self.results = list(filter(is_relevant, self.results))

    def __str__(self):
        s = ''
        for result in self.results:
            s += str(result)
        return s

    def log(self):
        logger = logging.getLogger(__name__)
        for result in self.results:
            logger.info(str(result))

    def map_result_category(self, results: List[SearchResult], category: str) -> List[SearchResult]:
        return list(map(
            lambda result: SearchResult(url=result.url, title=result.title, caption=result.caption, category=category),
            results
        ))
