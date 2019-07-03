from unittest import TestCase

from bing_search import bing_search


class TestBingSearch(TestCase):
    def test_bing_search(self):
        results = bing_search('facebook')
        self.assertNotEqual(results, [])
        self.assertIn('Facebook', results[0].title)
