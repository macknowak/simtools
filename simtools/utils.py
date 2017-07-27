# -*- coding: utf-8 -*-
"""Miscellaneous utilities.

Miscellaneous utilities provide saving software versions to a JSON file.
"""

import collections
import json


def save_versions(filename, versions, **kwargs):
    """Save software versions to a file."""
    DEFAULT_INDENT = 4

    # If necessary, validate version information
    if not isinstance(versions, dict):
        try:
            iter(versions)
        except TypeError:
            raise TypeError("'versions' is not iterable.")

    # If necessary, validate extra keyword arguments
    if kwargs:
        for arg in ('obj', 'fp'):
            if arg in kwargs:
                raise TypeError("save_versions() got an unexpected keyword "
                                "argument '{}'.".format(arg))

    # If necessary, convert version information to an ordered dictionary
    if not isinstance(versions, dict):
        try:
            versions = collections.OrderedDict(versions)
        except ValueError:
            raise ValueError("Unpacking 'versions' failed.")

    # Determine indentation
    indent = kwargs.pop('indent', DEFAULT_INDENT)

    # Save parameters to a JSON file
    with open(filename, 'w') as versions_file:
        json.dump(versions, versions_file, indent=indent, **kwargs)
