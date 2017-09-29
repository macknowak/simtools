#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Parameter exporter.

Parameter exporter is a console script that exports parameters of multiple
simulations to a file. It first loads from a text file the names of parameters
to be exported along with an optional mapping that defines how these names
should be substituted with different ones, then loads from another text file
the names of relevant simulation directories, and finally, as the parameters
are collected by traversing the simulation directories and loading appropriate
parameter files, it exports them to a file.
"""

__all__ = ['main']

import argparse
import os
import sys

from simtools.argparse import dir_r_type, file_r_type
from simtools.params import export_params, load_paramnames
from simtools.simrun import load_sim_dirnames

extra_options = {
    'csv': {
        "--dialect": 'dialect',
        "--no-header": 'with_header'
        },
    'json': {
        "--compact": 'compact',
        "--indent": 'indent'
        }
    }
supported_filefmts = extra_options.keys()


def getfilefmt(filename):
    """Retrieve file format based on file extension."""
    return os.path.splitext(filename)[1].lower()[1:]


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Export parameters of multiple simulations to a file.")
    parser.add_argument(
        "-m", "--master-dir", metavar="MASTERDIR",
        dest='sim_master_dirname', type=dir_r_type,
        help="parent directory of simulation directories")
    parser.add_argument(
        "-n", "--number",
        dest='with_numbers', action='store_true', default=False,
        help="include record numbers")
    parser.add_argument(
        "paramnames_filename", metavar="PARAMNAMEFILE",
        type=file_r_type,
        help="file with names of parameters to export")
    parser.add_argument(
        "sim_dirnames_filename", metavar="SIMDIRFILE",
        type=file_r_type,
        help="file with names of simulation directories")
    parser.add_argument(
        "params_filename", metavar="PARAMFILE",
        help="name of parameter file")
    parser.add_argument(
        "export_filename", metavar="EXPORTFILE",
        help="file to export parameters to")
    parser.add_argument(
        "--dialect", metavar="DIALECT",
        dest='dialect', default=argparse.SUPPRESS,
        help="use DIALECT when exporting to CSV file")
    parser.add_argument(
        "--no-header",
        dest='with_header', action='store_false', default=argparse.SUPPRESS,
        help="do not include header when exporting to CSV file")
    indent_group = parser.add_mutually_exclusive_group()
    indent_group.add_argument(
        "--compact",
        dest='compact', action='store_true', default=argparse.SUPPRESS,
        help="use the most compact representation when exporting to JSON file")
    indent_group.add_argument(
        "--indent", metavar="INDENT",
        dest='indent', type=int, default=argparse.SUPPRESS,
        help="indent each level by INDENT when exporting to JSON file")
    args = parser.parse_args()
    export_filefmt = getfilefmt(args.export_filename)
    if export_filefmt not in supported_filefmts:
        parser.error("{}: file format not supported"
                     "".format(args.export_filename))
    for filefmt, options in extra_options.items():
        if filefmt != export_filefmt:
            for arg, dest in options.items():
                if hasattr(args, dest):
                    parser.error(
                        "argument {0}: not allowed when exporting to {1} file"
                        "".format(arg, export_filefmt.upper()))
    if hasattr(args, 'compact'):
        args.indent = None
        del args.compact
    return args


def main():
    # Process command line arguments
    args = parse_args()

    # Determine extra options depending on the format of the export file
    export_filefmt = getfilefmt(args.export_filename)
    options = {}
    for opt in extra_options[export_filefmt].values():
        try:
            options[opt] = getattr(args, opt)
        except AttributeError:
            pass

    # Load parameter names and mapping of parameter names from the file with
    # names of parameters
    paramnames, paramnames_map = load_paramnames(args.paramnames_filename)
    if not paramnames_map:
        paramnames_map = None

    # Load names of simulation directories from the file with names of
    # simulation directories
    sim_dirnames = load_sim_dirnames(args.sim_dirnames_filename)

    # Determine paths to parameter files
    if args.sim_master_dirname is not None:
        params_paths = [os.path.join(args.sim_master_dirname, sim_dirname,
                                     args.params_filename)
                        for sim_dirname in sim_dirnames]
    else:
        params_paths = [os.path.join(sim_dirname, args.params_filename)
                        for sim_dirname in sim_dirnames]
    for param_path in params_paths:
        if not os.path.isfile(param_path):
            sys.exit("{0}: error: parameter file: no such file: "
                     "'{1}'".format(os.path.basename(sys.argv[0]), param_path))

    # Export parameters of multiple simulations to a file
    export_params(args.export_filename, params_paths, paramnames,
                  paramnames_map, args.with_numbers, **options)


if __name__ == '__main__':
    sys.exit(main())
