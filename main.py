import argparse

from osint.osint import Osint, filepath


def parse_args():
    parser = argparse.ArgumentParser(description='Python OSINT')
    parser.add_argument('-u', '--username',
                        help='Username (nickname online)', type=str)
    parser.add_argument('-e', '--email',
                        help='Email address', type=str)
    parser.add_argument('-f', '--firstname',
                        help='Firstname (must come with a lastname as well)', type=str)
    parser.add_argument('-l', '--lastname',
                        help='Lastname (must come with a firstname as well)', type=str)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    osint = Osint(username=args.username, email=args.email, firstname=args.firstname, lastname=args.lastname)
    print('Searching {}...'.format(args))
    osint.search()
    osint.log()
    print('Results available in {}...'.format(filepath))
