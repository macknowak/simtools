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


def file_r_type(filename):
    """Check if file exists and is readable."""
    if not os.path.isfile(filename):
        raise argparse.ArgumentTypeError(
            "no such file: '{}'".format(filename))
    if not os.access(filename, os.R_OK):
        raise argparse.ArgumentTypeError(
            "permission denied: '{}'".format(filename))
    return filename


def dir_r_type(dirname):
    """Check if directory exists and is readable."""
    if not os.path.isdir(dirname):
        raise argparse.ArgumentTypeError(
            "no such directory: '{}'".format(dirname))
    if not os.access(dirname, os.R_OK):
        raise argparse.ArgumentTypeError(
            "permission denied: '{}'".format(dirname))
    return dirname


def dir_w_type(dirname):
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
            'type': dir_w_type,
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
            'type': file_r_type,
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


def parse_args(allowed_options, only_long_names=False, parser=None):
    """Parse command line arguments."""
    parser = _make_parser(allowed_options, allow_extra_args=False,
                          only_long_names=only_long_names, parser=parser)
    return Dict(vars(parser.parse_args()))


def parse_known_args(allowed_options, only_long_names=False, parser=None):
    """Parse command line arguments with extra arguments retained."""
    parser = _make_parser(allowed_options, allow_extra_args=True,
                          only_long_names=only_long_names, parser=parser)
    args, extra_args = parser.parse_known_args()
    return Dict(vars(args)), extra_args


def _make_parser(allowed_options, allow_extra_args, only_long_names, parser):
    """Create or update parser."""
    # If necessary, create parser
    if parser is None:
        parser = argparse.ArgumentParser()

    # Check if all allowed options are supported
    unsupported_options = set(allowed_options) - set(all_options)
    if unsupported_options:
        parser.error(
            "unsupported options: {}".format(' '.join(unsupported_options)))

    # Supply the parser with descriptions of arguments corresponding to the
    # allowed options
    for option in allowed_options:
        opt = all_options[option]
        if only_long_names:
            parser.add_argument(opt['arg'][1], **opt['spec'])
        else:
            parser.add_argument(*opt['arg'], **opt['spec'])

    return parser
