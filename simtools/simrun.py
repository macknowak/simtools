# -*- coding: utf-8 -*-
"""Simulation launch services.

Simulation launch services provide generating simulation id based on local date
and time.
"""

import time


def generate_sim_id():
    """Generate simulation id based on local date and time."""
    t = time.localtime()
    sim_id = "{0:04}{1:02}{2:02}_{3:02}{4:02}{5:02}".format(
        t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    return sim_id
