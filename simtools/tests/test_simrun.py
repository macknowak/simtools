# -*- coding: utf-8 -*-
"""Unit tests of simulation launch services."""

import os
import time

import pytest

from simtools.simrun import generate_sim_id, generate_sim_dirname, make_dirs


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
    sim_master_dirname = "simulations"
    data_dirname = "data"

    with tmpdir.as_cwd():
        # No simulation master directory, no data directory
        sim_path = make_dirs(sim_dirname)
        assert sim_path == sim_dirname
        assert os.path.isdir(sim_path)

        # Simulation master directory but no data directory
        sim_path = make_dirs(sim_dirname, sim_master_dirname)
        assert sim_path == os.path.join(sim_master_dirname, sim_dirname)
        assert os.path.isdir(sim_path)

        # Simulation master directory and data directory
        sim_path = make_dirs(sim_dirname, sim_master_dirname, data_dirname)
        assert sim_path == os.path.join(sim_master_dirname, sim_dirname)
        assert os.path.isdir(os.path.join(sim_path, data_dirname))
