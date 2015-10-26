#!/usr/bin/env python

"""
A wrapper around Wappalyzer:
Checks which framework(s) a (list of) website(s) use(s)
"""


from __future__ import absolute_import
from __future__ import print_function
import argparse
import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
import sys
import textwrap
import urlparse

from Wappalyzer import Wappalyzer, WebPage

__author__ = "Peter Mosmans"
__copyright__ = "Copyright 2015, Go Forward"
__license__ = "GPL"
__version__ = "0.0.2"
__maintainer__ = "Peter Mosmans"
__contact__ = "support@go-forward.net"
__status__ = "Development"


def analyze_url(host, parameters):
    """
    Analyzes an URL using wappalyzer and prints the results.
    """
    url = host
    headers = {}
    verify = True
    proxies = {}
    if not urlparse.urlparse(url).scheme:
        url = 'http://{0}'.format(url)
    # try:
    # user_agent
    wappalyzer = Wappalyzer.latest()
    print(parameters)
    if parameters['username'] and parameters['password']:
        if parameters['digest']:
            auth = HTTPDigestAuth(parameters['username'], parameters['password'])
        else:
            auth = HTTPBasicAuth(parameters['username'], parameters['password'])
    if parameters['proxy']:
        proxies['http'] = parameters['proxy']
        proxies['https'] = parameters['proxy']
    if parameters.has_key('no_validate'):
        requests.packages.urllib3.disable_warnings()
        verify = False
    page = requests.get(url, auth=auth, proxies=proxies, verify=verify)

    if page.status_code == 200:
        webpage = WebPage(url, page.text, headers)
        print('[+] {0} {1}'.format(host, wappalyzer.analyze(webpage)))
    # except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        # print('[-] Could not connect to {0}'.format(url))
    else:
        print('Got result {0} - cannot analyze that...'.format(page.status_code))
    sys.stdout.flush()


def parse_arguments():
    """
    Parses command line arguments.
    """
    parameters = {}
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
    parser.add_argument('--username', action='store', type=str,
                        help='username to connect to website')
    parser.add_argument('--password', action='store', type=str,
                        help='password to connect to website')
    parser.add_argument('--digest', action='store_true',
                        help='use digest authentication mechanism')
    parser.add_argument('--proxy', action='store', type=str,
                        help='use a proxy for the request')
    parser.add_argument('--novalidate', action='store_true',
                        help='do not validate the SSL certificate')
    args = parser.parse_args()
    parameters['filename'] = args.file
    if not parameters['filename']:
        if not args.URL:
            parser.print_help()
            sys.exit(1)
    parameters['username'] = args.username
    parameters['password'] = args.password
    parameters['digest'] = args.digest
    parameters['proxy'] = args.proxy
    parameters['no_validate'] = args.novalidate
    return args.URL, parameters


def main():
    """
    Main program loop.
    """
    url, parameters = parse_arguments()
    if parameters['filename']:
        try:
            for url in open(parameters['filename'], 'r'):
                analyze_url(url.rstrip(), parameters)
        except IOError:
            print('[-] Could not open {0}'.format(parameters['filename']))
            sys.exit(-1)
    else:
        analyze_url(url, parameters)


if __name__ == "__main__":
    main()
