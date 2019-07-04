from unittest import TestCase

from osint.osint import Osint


class TestOsint(TestCase):
    def test_search(self):
        for result in Osint(username='zboubinours', email='rodguillaume@tuta.io', firstname='Rod', lastname='Guillaume').search():
            print(result)
