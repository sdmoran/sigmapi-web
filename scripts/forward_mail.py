#!/usr/bin/python3.6
"""
Forward email to the web app.
"""
import fileinput
import requests


_API_URL = (
    'http://localhost:8000/secure/mailinglists/sendmail/'
)


def main():
    all_input = ''.join(line for line in fileinput.input())
    data = {
        'key': None,
        'data': all_input,
    }
    response = requests.post(_API_URL, data=data)
    return 0 if 200 < response.status_code < 299 else 1


exit(main())
