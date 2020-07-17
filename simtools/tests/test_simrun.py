# -*- coding: utf-8 -*-
"""Unit tests of simulation launch services."""

import os
import time

import pytest

from simtools.simrun import (generate_sim_id, generate_sim_dirname,
                             load_sim_dirnames, make_dirs, norm_executable)


@pytest.fixture
def local_time(monkeypatch):
    t = time.strptime("2000-10-30 07:08:09", "%Y-%m-%d %H:%M:%S")
    monkeypatch.setattr(time, 'localtime', lambda: t)


def test_generate_sim_id(local_time):
    sim_id = generate_sim_id()
    assert sim_id == "20001030_070809"


def test_generate_sim_dirname(local_time):
    # Default
    sim_dirname = generate_sim_dirname()
    assert sim_dirname == "20001030_070809"

    # Temporary directory, no simulation id
    sim_dirname = generate_sim_dirname(tmp=True)
    assert sim_dirname == "_20001030_070809"

    # Simulation id
    sim_dirname = generate_sim_dirname(sim_id="20001030_070809")
    assert sim_dirname == "20001030_070809"

    # Temporary directory, simulation id
    sim_dirname = generate_sim_dirname(tmp=True, sim_id="20001030_070809")
    assert sim_dirname == "_20001030_070809"


def test_make_dirs(tmpdir):
    sim_dirname = "20001030_070809"

    with tmpdir.as_cwd():
        # No simulation master directory, no data directory
        sim_path = make_dirs(sim_dirname)
        assert sim_path == sim_dirname
        assert os.path.isdir(sim_path)

        # Simulation master directory but no data directory
        sim_master_dirname = "simulations1"
        sim_path = make_dirs(sim_dirname, sim_master_dirname)
        assert sim_path == os.path.join(sim_master_dirname, sim_dirname)
        assert os.path.isdir(sim_path)

        # Simulation master directory and data directory
        sim_master_dirname = "simulations2"
        data_dirname = "data"
        sim_path = make_dirs(sim_dirname, sim_master_dirname, data_dirname)
        assert sim_path == os.path.join(sim_master_dirname, sim_dirname)
        assert os.path.isdir(os.path.join(sim_path, data_dirname))


def test_make_dirs_exist(tmpdir):
    sim_dirname = "20001030_070809"
    tmpdir.mkdir(sim_dirname)

    with tmpdir.as_cwd():
        # No data directory
        with pytest.raises(OSError):
            sim_path = make_dirs(sim_dirname)

        # Data directory
        data_dirname = "data"
        with pytest.raises(OSError):
            sim_path = make_dirs(sim_dirname, data_dirname=data_dirname)


@pytest.mark.parametrize('executable, normal_executable', [
    ("/myexec", ["/myexec"]),
    ("/myexec -x", ["/myexec", "-x"])])
def test_norm_executable_abs(executable, normal_executable):
    normalized_executable = norm_executable(executable)
    assert normalized_executable == normal_executable


@pytest.mark.parametrize('executable, normal_executable', [
    ("myexec", ["myexec"]),
    ("myexec -x", ["myexec", "-x"])])
def test_norm_executable_rel_nonexist(tmpdir, executable, normal_executable):
    with tmpdir.as_cwd():
        normalized_executable = norm_executable(executable)
        assert normalized_executable == normal_executable


@pytest.mark.parametrize('executable, normal_executable', [
    ("myexec", [""]),
    ("myexec -x", ["", "-x"])])
def test_norm_executable_rel_exist(tmpdir, executable, normal_executable):
    myexec = tmpdir.join("myexec")
    myexec.write("")
    normal_executable[0] = str(myexec)

    with tmpdir.as_cwd():
        normalized_executable = norm_executable(executable)
        assert normalized_executable == normal_executable


def test_load_sim_dirnames(tmpdir):
    sim_dirnames_file = tmpdir.join("dirnames.txt")
    sim_dirnames_file.write(
"""# Simulation directories

20001020_020304
    20001020_030405
simulations/20001020_040506
    simulations/20001020_050607/
simulations\\20001020_060708\\
    simulations\\20001020_070809

    # End of simulation directories
""")

    sim_dirnames = load_sim_dirnames(str(sim_dirnames_file))
    assert len(sim_dirnames) == 6
    assert sim_dirnames[0] == "20001020_020304"
    assert sim_dirnames[1] == "20001020_030405"
    assert sim_dirnames[2] == os.path.join("simulations", "20001020_040506")
    assert sim_dirnames[3] == os.path.join("simulations", "20001020_050607")
    assert sim_dirnames[4] == os.path.join("simulations", "20001020_060708")
    assert sim_dirnames[5] == os.path.join("simulations", "20001020_070809")
