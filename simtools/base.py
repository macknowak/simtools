# -*- coding: utf-8 -*-
"""Assorted base data structures.

Assorted base data structures provide a dictionary with access to values
through attributes.
"""


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
