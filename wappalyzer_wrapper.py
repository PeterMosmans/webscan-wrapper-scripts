#!/usr/bin/env python

"""
A wrapper around Wappalyzer:
Checks which framework(s) a (list of) website(s) use(s)
"""


from __future__ import absolute_import
from __future__ import print_function
import argparse
import requests
import sys
import textwrap
import urlparse

from Wappalyzer import Wappalyzer, WebPage

__author__ = "Peter Mosmans"
__copyright__ = "Copyright 2015, Go Forward"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Peter Mosmans"
__contact__ = "support@go-forward.net"
__status__ = "Development"


def analyze_url(url):
    """
    Analyzes an URL using wappalyzer and prints the results.
    """
    if not urlparse.urlparse(url).scheme:
        url = 'http://{0}'.format(url)
    try:
        wappalyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_url(url)
        print('[+] {0}: {1}'.format(url, wappalyzer.analyze(webpage)))
    except requests.exceptions.ConnectionError:
        print('[-] Could not connect to {0}'.format(url))
    sys.stdout.flush()


def parse_arguments():
    """
    Parses command line arguments.
    """
    input_file = None
    parser = argparse.ArgumentParser(formatter_class=argparse.
                                     RawDescriptionHelpFormatter,
                                     description=textwrap.dedent('''\
Checks which framework(s) a website uses (a wrapper around Wappalyzer)

Copyright (C) 2015 Peter Mosmans [Go Forward]
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.'''))
    parser.add_argument('URL', nargs='?', type=str, help='the URL to check')
    parser.add_argument('--file', action='store', type=str,
                        help='file containing urls to check')
    args = parser.parse_args()
    if args.file:
        input_file = args.file
    else:
        if not args.URL:
            parser.print_help()
            sys.exit(1)
    return args.URL, input_file


def main():
    """
    Main program loop.
    """
    url, input_file = parse_arguments()
    if input_file:
        try:
            for url in open(input_file, 'r'):
                analyze_url(url.rstrip())
        except IOError:
            print('[-] Could not open {0}'.format(input_file))
            sys.exit(-1)
    else:
        analyze_url(url)


if __name__ == "__main__":
    main()
