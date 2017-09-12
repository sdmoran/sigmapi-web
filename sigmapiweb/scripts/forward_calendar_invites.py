#!/usr/bin/python3.6
"""
Forward calendar invites to the web app.
"""
import fileinput
import requests


_CALANDAR_INVITE_FORWARD_URL = (
    'http://localhost:8000/secure/calendar/sendinvite/'
)


def main():
    all_input = ''.join(line for line in fileinput.input())
    data = {
        'key': None,
        'data': all_input,
    }
    response = requests.post(_CALANDAR_INVITE_FORWARD_URL, data=data)
    return 0 if 200 < response.status_code < 299 else 1


exit(main())
