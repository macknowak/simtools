# -*- coding: utf-8 -*-
"""Miscellaneous utilities.

Miscellaneous utilities provide the following functionality:

- saving platform information to a JSON file;
- saving software versions to a JSON file.
"""

import collections
import json
import platform

from simtools.base import is_iterable


def save_platform(filename, **kwargs):
    """Save platform information to a file."""
    DEFAULT_INDENT = 4

    # If necessary, validate extra keyword arguments
    if kwargs:
        for arg in ('obj', 'fp'):
            if arg in kwargs:
                raise TypeError("save_platform() got an unexpected keyword "
                                "argument '{}'.".format(arg))

    # Retrieve platform information
    platform_info = collections.OrderedDict()
    platform_info['node'] = platform.node()
    platform_info['machine'] = platform.machine()
    platform_info['processor'] = platform.processor()
    platform_info['system'] = platform.system()
    platform_info['version'] = platform.version()
    platform_info['release'] = platform.release()

    # Determine indentation
    indent = kwargs.pop('indent', DEFAULT_INDENT)

    # Save platform information to a JSON file
    with open(filename, 'w') as platform_file:
        json.dump(platform_info, platform_file, indent=indent, **kwargs)


def save_versions(filename, versions_info, **kwargs):
    """Save software versions to a file."""
    DEFAULT_INDENT = 4

    # If necessary, validate software version information
    if not isinstance(versions_info, dict):
        if not is_iterable(versions_info):
            raise TypeError("'versions_info' is not iterable.")

    # If necessary, validate extra keyword arguments
    if kwargs:
        for arg in ('obj', 'fp'):
            if arg in kwargs:
                raise TypeError("save_versions() got an unexpected keyword "
                                "argument '{}'.".format(arg))

    # If necessary, convert software version information to an ordered
    # dictionary
    if not isinstance(versions_info, dict):
        try:
            versions_info = collections.OrderedDict(versions_info)
        except ValueError:
            raise ValueError("Unpacking 'versions_info' failed.")

    # Determine indentation
    indent = kwargs.pop('indent', DEFAULT_INDENT)

    # Save software version information to a JSON file
    with open(filename, 'w') as versions_file:
        json.dump(versions_info, versions_file, indent=indent, **kwargs)
