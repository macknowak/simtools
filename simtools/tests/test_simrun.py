# -*- coding: utf-8 -*-
"""Unit tests of simulation launch services."""

import time

from simtools.simrun import generate_sim_id


def test_generate_sim_id(monkeypatch):
    t = time.strptime("2000-10-30 07:08:09", "%Y-%m-%d %H:%M:%S")
    monkeypatch.setattr(time, 'localtime', lambda: t)

    sim_id = generate_sim_id()
    assert sim_id == "20001030_070809"
