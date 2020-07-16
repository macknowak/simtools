# -*- coding: utf-8 -*-
"""Assorted base data structures and common functions.

Assorted base data structures and common functions provide the following data
structure:

- dictionary with access to values through attributes.

They also provide the following functionality:

- checking if object is an iterable.
"""


def is_iterable(obj):
    """Check if object is an iterable."""
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True


class Dict(dict):
    """Dictionary with access to values through attributes."""

    def __getattr__(self, name):
        """Retrieve value through an attribute."""
        try:
            return self[name]
        except KeyError:
            return super(Dict, self).__getattribute__(name)

    def __setattr__(self, name, value):
        """Set value through an attribute."""
        self[name] = value

    def __delattr__(self, name):
        """Delete value through an attribute."""
        try:
            del self[name]
        except KeyError:
            return super(Dict, self).__getattribute__(name)
