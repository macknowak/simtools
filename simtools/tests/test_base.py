# -*- coding: utf-8 -*-
"""Unit tests of assorted base data structures."""

import pytest

from simtools.base import Dict


def test_dict_attr_access():
    d = Dict()

    d['a'] = 1
    assert d.a == 1

    d.b = 2
    assert d['b'] == 2

    with pytest.raises(AttributeError):
        d.c


def test_dict_attr_deletion():
    d = Dict()
    d['a'] = 1

    del d.a
    with pytest.raises(KeyError):
        d['a']
    with pytest.raises(AttributeError):
        d.a
