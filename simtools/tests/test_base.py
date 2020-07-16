# -*- coding: utf-8 -*-
"""Unit tests of assorted base data structures and common functions."""

import pytest

from simtools.base import Dict, is_iterable, is_string


def test_is_iterable():
    # List of integers
    obj = [1, 2, 3]
    assert is_iterable(obj) == True

    # Tuple of integers
    obj = 1, 2, 3
    assert is_iterable(obj) == True

    # List of strings
    obj = ["abc", "def", "ghi"]
    assert is_iterable(obj) == True

    # Tuple of strings
    obj = "abc", "def", "ghi"
    assert is_iterable(obj) == True

    # Dictionary
    obj = {1: "abc", 2: "def", 3: "ghi"}
    assert is_iterable(obj) == True

    # Integer
    obj = 1
    assert is_iterable(obj) == False

    # String
    obj = "abc"
    assert is_iterable(obj) == True


def test_is_string():
    # String
    obj = "abc"
    assert is_string(obj) == True

    # Integer
    obj = 1
    assert is_string(obj) == False

    # List of strings
    obj = ["abc", "def", "ghi"]
    assert is_string(obj) == False

    # Dictionary
    obj = {"abc": 1, "def": 2, "ghi": 3}
    assert is_string(obj) == False


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
