# -*- coding: utf-8 -*-
"""Simulation launch services.

Simulation launch services provide the following functionality:

- generating simulation id based on local date and time;
- generating simulation directory name;
- creating directory structure for simulation.
"""

import os
import time

TMP_DIR_PREFIX = "_"


def generate_sim_id():
    """Generate simulation id based on local date and time."""
    t = time.localtime()
    sim_id = "{0:04}{1:02}{2:02}_{3:02}{4:02}{5:02}".format(
        t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    return sim_id


def generate_sim_dirname(tmp=False, sim_id=None):
    """Generate simulation directory name."""
    if not sim_id:
        sim_id = generate_sim_id()
    return sim_id if not tmp else TMP_DIR_PREFIX + sim_id


def make_dirs(sim_dirname, sim_master_dirname=None, data_dirname=None):
    """Create directory structure for simulation."""
    if sim_master_dirname is None:
        sim_master_dirname = ""
    if data_dirname is None:
        data_dirname = ""
    sim_path = os.path.join(sim_master_dirname, sim_dirname)
    os.makedirs(os.path.join(sim_path, data_dirname))
    return sim_path
