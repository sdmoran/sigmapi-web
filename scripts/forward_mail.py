#!/usr/bin/python3.6
"""
Forward email to the web app.
"""
import fileinput
import os
import requests


def main():
    """
    Forward STDIN to the mailing lists sendmail API.
    """
    api_root = os.environ.get(
        'MAILING_LISTS_API_ROOT',
        'http://localhost:8000/',
    )
    api_key = os.environ.get('MAILING_LISTS_API_KEY')
    all_input = ''.join(line for line in fileinput.input())
    data = {
        'key': api_key,
        'data': all_input,
    }
    api_url = api_root + 'secure/mailinglists/sendmail/'
    response = requests.post(api_url, data=data)
    return 0 if 200 < response.status_code < 299 else 1


exit(main())
