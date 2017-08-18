"""
Settings for Sigma Pi, Gamma Iota chapter website.

Try to import production settings, which should only be available on the
production server. If that fails, import local settings. If that fails,
fall back to development settings.
"""
# pylint: disable=wildcard-import,unused-wildcard-import
try:
    from .prod import *
except ImportError:
    try:
        from .local import *
    except ImportError:
        from .dev import *


MANAGERS = ADMINS
