# -*- coding: utf-8 -*-
"""Unit tests of simulation launch services."""

import time

import pytest

from simtools.simrun import generate_sim_id, generate_sim_dirname


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
