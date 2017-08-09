# -*- coding: utf-8 -*-
"""Simulation launch services.

Simulation launch services provide the following functionality:

- generating simulation id based on local date and time;
- generating simulation directory name;
- creating directory structure for simulation;
- normalizing the format of executable;
- launching simulation.
"""

import os
import shlex
import subprocess
import time

from simtools.argparse import all_options as options

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


def run_sim(model_filename, params_filename=None, sim_id=None,
            data_dirname=None, executable=None):
    """Launch simulation."""
    cmd = []
    if executable:
        try:
            basestring
        except NameError:
            basestring = str
        if isinstance(executable, basestring):
            cmd.append(executable)
        else:
            try:
                iter(executable)
            except TypeError:
                raise TypeError(
                    "'executable' is neither a string nor iterable.")
            cmd += executable
    cmd.append(model_filename)
    if params_filename:
        cmd += [options['params_filename']['arg'][0], params_filename]
    if sim_id:
        cmd += [options['sim_id']['arg'][0], sim_id]
    if data_dirname:
        cmd += [options['data_dirname']['arg'][0], data_dirname]
    cmd.append(options['save_data']['arg'][0])
    return subprocess.call(cmd)


def norm_executable(executable):
    """Normalize the format of executable."""
    # Split executable name and arguments
    executable = shlex.split(executable)

    # If necessary, determine the absolute path to the executable
    if not os.path.isabs(executable[0]) and os.path.isfile(executable[0]):
        executable[0] = os.path.abspath(executable[0])

    return executable
