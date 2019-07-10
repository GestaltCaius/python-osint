from unittest import TestCase

from osint.osint import Osint, filepath


class TestOsint(TestCase):
    def test_search(self):
        osint = Osint(username='zboubinours', email='rodguillaume@tuta.io', firstname='Rod', lastname='Guillaume')
        osint.search()
        print(str(osint))

    def test_log(self):
        osint = Osint(username='zboubinours', email='rodguillaume@tuta.io', firstname='Rod', lastname='Guillaume')
        osint.search()
        osint.log()
        with open(filepath, 'r') as f:
            print(f.read())

