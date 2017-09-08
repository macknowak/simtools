#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Random seed generator.

Random seed generator is a console script that generates random seed using
OS-specific randomness source and then prints it. The generated random seed can
have a specified number of bytes or otherwise its number of bytes is determined
to match the number of bytes used by the largest positive integer supported by
the platform.
"""

from __future__ import print_function

__all__ = ['main']

import argparse
import sys

from simtools.random import MAX_N_BYTES, generate_seed


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate random seed using OS-specific randomness "
                    "source.")
    parser.add_argument(
        "-b", "--bytes", metavar="BYTES",
        dest='n_bytes', type=int,
        help="generate random seed that is BYTES bytes long")
    args = parser.parse_args()
    if args.n_bytes is not None:
        if args.n_bytes <= 0:
            parser.error("argument -b/--bytes: invalid value: expected "
                         "positive number")
        elif args.n_bytes > MAX_N_BYTES:
            parser.error("argument -b/--bytes: invalid value: expected number "
                         "not greater than {}".format(MAX_N_BYTES))
    return args


def main():
    # Process command line arguments
    args = parse_args()

    # Generate random seed and print it
    print(generate_seed(args.n_bytes))


if __name__ == '__main__':
    sys.exit(main())
