"""
Constants relating to access to mailing lists.
"""

# Types
ACCESS_SUBSCRIBE = 'sub'
ACCESS_SEND = 'snd'


# Meta
ACCESS_CHOICE_LEN = 3
ACCESS_DICT = {
    ACCESS_SUBSCRIBE: 'Subscribe',
    ACCESS_SEND: 'Send',
}
ACCESS_CHOICES = frozenset(ACCESS_DICT.items())
