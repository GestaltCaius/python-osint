from unittest import TestCase

from bing_search.bing_search import bing_search


class TestBingSearch(TestCase):
    def test_bing_search(self):
        """
        Checks if bing_search returns results
        """
        results = bing_search('facebook')
        self.assertNotEqual(results, [])
        self.assertIn('facebook', results[0].title.lower())

    def test_search_results_format(self):
        """
        Checks bing search result string format
        """
        for r in bing_search('facebook'):
            print(r)
