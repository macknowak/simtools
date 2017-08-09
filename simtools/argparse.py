# -*- coding: utf-8 -*-
"""Command line argument parsing services.

Command line argument parsing services provide the following functionality:

- specifying which predefined options are supported;
- parsing command line arguments to populate supported options.
"""

from __future__ import absolute_import

import argparse
import os

from simtools.base import Dict


def _directory_type(dirname):
    """Check if directory exists and is writable."""
    if not os.path.isdir(dirname):
        raise argparse.ArgumentTypeError(
            "no such directory: '{}'".format(dirname))
    if not os.access(dirname, os.W_OK):
        raise argparse.ArgumentTypeError(
            "permission denied: '{}'".format(dirname))
    return dirname


all_options = {
    'data_dirname': {
        'arg': ["-d", "--data-dir"],
        'spec': {
            'metavar': "DIR",
            'dest': 'data_dirname',
            'type': _directory_type,
            'help': "data directory"
            }
        },
    'only_test_params': {
        'arg': ["-t", "--only-params"],
        'spec': {
            'action': 'store_true',
            'dest': 'only_test_params',
            'help': "only verify parameters and exit"
            }
        },
    'params_filename': {
        'arg': ["-p", "--params"],
        'spec': {
            'metavar': "FILE",
            'dest': 'params_filename',
            'help': "parameter file"
            }
        },
    'save_data': {
        'arg': ["-s", "--save"],
        'spec': {
            'action': 'store_true',
            'dest': 'save_data',
            'help': "save data"
            }
        },
    'sim_id': {
        'arg': ["-i", "--simid"],
        'spec': {
            'metavar': "ID",
            'dest': 'sim_id',
            'help': "simulation id"
            }
        }
    }


def parse_args(allow_options):
    """Parse command line arguments."""
    # Check if all allowed options are supported
    parser = argparse.ArgumentParser()
    unsupported_options = set(allow_options) - set(all_options)
    if unsupported_options:
        parser.error(
            "unsupported options: {}".format(' '.join(unsupported_options)))

    # Process command line arguments
    for option in allow_options:
        opt = all_options[option]
        parser.add_argument(*opt['arg'], **opt['spec'])
    return Dict(vars(parser.parse_args()))
