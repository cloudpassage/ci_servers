from __future__ import print_function

import sys


class Utility(object):
    """This is a collection of widely-used functions"""

    @classmethod
    def date_to_iso8601(cls, date_obj):
        """Returns an ISO8601-formatted string for datetime arg"""
        retval = date_obj.isoformat()
        return retval

    @classmethod
    def log_stdout(cls, message, component="CI_Servers"):
        """Log messages to stdout.

        Args:
            message(str): Message to be logged to stdout.
            component(str): Component name. Defaults to "CI_Servers".
        """
        out = "%s: %s" % (component, message)
        print(out, file=sys.stdout)
        return

    @classmethod
    def log_stderr(cls, message, component="CI_Servers"):
        """Log messages to stderr.

        Args:
            message(str): Message to be logged to stdout.
            component(str): Component name. Defaults to "CI_Servers".
        """
        out = "%s: %s" % (component, message)
        print(out, file=sys.stderr)
        return
