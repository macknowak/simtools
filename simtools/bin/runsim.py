#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simulation launcher.

Simulation launcher is a console script that launches model simulation in a
designated directory. It first creates an appropriate directory structure
including the simulation directory, generating simulation id if necessary, then
changes the current working directory to the simulation directory, and finally
launches a simulation as a child process, passing all relevant command line
arguments to the model. Optionally, before launching the simulation, it can
also copy the model file as well as an optional parameter file to the
simulation directory.
"""

__all__ = ['main']

import argparse
import os
import shutil
import sys

from simtools.argparse import file_r_type
from simtools.simrun import (TMP_DIR_PREFIX, generate_sim_dirname,
                             generate_sim_id, make_dirs, norm_executable,
                             run_sim)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Launch model simulation.")
    parser.add_argument(
        "-e", "--exec", metavar="EXECUTABLE",
        dest='executable',
        help="use EXECUTABLE to run the model file")
    parser.add_argument(
        "-m", "--master-dir", metavar="MASTERDIR",
        dest='sim_master_dirname',
        help="create simulation directory in the parent directory MASTERDIR, "
             "along with creating MASTERDIR if it does not exist")
    sim_dir_group = parser.add_mutually_exclusive_group()
    sim_dir_group.add_argument(
        "-s", "--sim-dir", metavar="SIMDIR",
        dest='sim_dirname',
        help="do not generate the name of the simulation directory and use "
             "SIMDIR instead")
    sim_dir_group.add_argument(
        "-t", "--tmp-dir",
        dest='tmp_dir', action='store_true',
        help="add prefix '{}' to the generated name of the simulation "
             "directory ".format(TMP_DIR_PREFIX))
    parser.add_argument(
        "-d", "--data-dir", metavar="DATADIR",
        dest='data_dirname',
        help="create data directory DATADIR in the simulation directory")
    parser.add_argument(
        "-p", "--params", metavar="PARAMFILE",
        dest='params_filename', type=file_r_type,
        help="parameter file")
    sim_id_group = parser.add_mutually_exclusive_group()
    sim_id_group.add_argument(
        "-i", "--simid", metavar="ID",
        dest='sim_id',
        help="do not generate simulation id and use ID instead")
    sim_id_group.add_argument(
        "--no-simid",
        dest='with_sim_id', action='store_false', default=True,
        help="do not pass simulation id to the model")
    copy_model_group = parser.add_mutually_exclusive_group()
    copy_model_group.add_argument(
        "--copy-model",
        dest='copy_model', action='store_true',
        help="copy the model file to the simulation directory")
    copy_model_group.add_argument(
        "--copy-model-rename", metavar="MODELFILECOPY",
        dest='copy_model_filename',
        help="copy the model file to the simulation directory as "
             "MODELFILECOPY")
    copy_params_group = parser.add_mutually_exclusive_group()
    copy_params_group.add_argument(
        "--copy-params",
        dest='copy_params', action='store_true',
        help="copy the parameter file to the simulation directory")
    copy_params_group.add_argument(
        "--copy-params-rename", metavar="PARAMFILECOPY",
        dest='copy_params_filename',
        help="copy the parameter file to the simulation directory as "
             "PARAMFILECOPY")
    parser.add_argument(
        "model_filename", metavar="MODELFILE",
        type=file_r_type,
        help="model file")
    parser.add_argument(
        "model_args", metavar="...",
        nargs=argparse.REMAINDER,
        help="optional additional arguments passed to the model file")
    args = parser.parse_args()
    if not args.executable and not os.access(args.model_filename, os.X_OK):
        parser.error("argument MODELFILE: permission denied: "
                     "'{}'".format(args.model_filename))
    if args.copy_params and not args.params_filename:
        parser.error("argument --copy-params: requires argument -p/--params")
    if args.copy_params_filename and not args.params_filename:
        parser.error("argument --copy-params-rename: requires argument "
                     "-p/--params")
    if args.copy_model_filename:
        args.copy_model = True
    if args.copy_params_filename:
        args.copy_params = True
    return args


def main():
    # Process command line arguments
    args = parse_args()

    # If necessary, determine simulation id
    if args.with_sim_id and not args.sim_id:
        sim_id = generate_sim_id()
    else:
        sim_id = args.sim_id

    # If necessary, generate simulation directory name
    if args.sim_dirname:
        sim_dirname = args.sim_dirname
    else:
        sim_dirname = generate_sim_dirname(args.tmp_dir, sim_id)

    # Create directory structure for simulation
    sim_path = make_dirs(sim_dirname, args.sim_master_dirname,
                         args.data_dirname)

    # Determine the absolute path to the model file
    model_path = os.path.abspath(args.model_filename)

    # If necessary, copy the model file to the simulation directory
    if args.copy_model:
        if args.copy_model_filename:
            shutil.copy(
                model_path, os.path.join(sim_path, args.copy_model_filename))
        else:
            shutil.copy(model_path, sim_path)

    # If necessary, determine the absolute path to the parameter file
    if args.params_filename:
        params_path = os.path.abspath(args.params_filename)
    else:
        params_path = None

    # If necessary, copy the parameter file to the simulation directory
    if args.copy_params:
        if args.copy_params_filename:
            shutil.copy(
                params_path, os.path.join(sim_path, args.copy_params_filename))
        else:
            shutil.copy(params_path, sim_path)

    # If necessary, normalize the format of the executable
    if args.executable:
        executable = norm_executable(args.executable)
    else:
        executable = None

    # Go to the simulation directory
    os.chdir(sim_path)

    # Launch simulation
    return run_sim(model_path, params_path, sim_id, args.data_dirname,
                   executable, args.model_args)


if __name__ == '__main__':
    sys.exit(main())
