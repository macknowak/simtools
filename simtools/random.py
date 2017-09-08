# -*- coding: utf-8 -*-
"""Random number services.

Random number services provide generating random seed using OS-specific
randomness source.
"""

import os
import sys

MAX_N_BYTES = 256


def generate_seed(n_bytes=None):
    """Generate random seed using OS-specific randomness source."""
    # If the number of bytes is specified, validate it, otherwise determine it
    # based on the largest positive integer supported by the platform
    if n_bytes is not None:
        if not isinstance(n_bytes, int):
            raise TypeError("n_bytes must be an integer or None")
        if n_bytes <= 0 or n_bytes > MAX_N_BYTES:
            raise ValueError("n_bytes must be positive and not greater "
                             "than {}".format(MAX_N_BYTES))
    else:
        n_bytes = (sys.maxsize.bit_length() + 1) / 8

    # Generate random bytes using OS-specific randomness source
    rand_bytes = os.urandom(n_bytes).encode('hex')

    # If the highest bit is 1, change it to 0 (to avoid using Python long
    # integers)
    highest_nibble_val = int(rand_bytes[0], 16)
    if highest_nibble_val > 7:
        rand_bytes = str(highest_nibble_val - 8) + rand_bytes[1:]

    return int(rand_bytes, 16)
