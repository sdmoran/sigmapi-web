#!/usr/bin/python3.6
"""
Forward calendar invites to the web app.
"""
import fileinput
import requests

from ..sigmapiweb.common.settings import (
    CALENDAR_INVITE_API_KEY,
    CALANDAR_INVITE_FORWARD_URL,
)


def main():
    all_input = '\n'.join(line for line in fileinput.input())
    data = {
        'key': CALENDAR_INVITE_API_KEY,
        'data': data,
    }
    requests.post(CALANDAR_INVITE_FORWARD_URL, data=data)


main()
