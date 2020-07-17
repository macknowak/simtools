# -*- coding: utf-8 -*-
"""Unit tests of random number services."""

import os
import sys

import pytest

from simtools.random import generate_seed


@pytest.mark.parametrize('maxsize, seed', [
    (2**31 - 1, 808464432),
    (2**63 - 1, 3472328296227680304)])
def test_generate_seed(monkeypatch, maxsize, seed):
    monkeypatch.setattr(os, 'urandom', lambda n: "\x30" * n)
    monkeypatch.setattr(sys, 'maxsize', maxsize)

    gen_seed = generate_seed()
    assert gen_seed == seed


@pytest.mark.parametrize('n_bytes, seed', [
    (4, 808464432),
    (8, 3472328296227680304)])
def test_generate_seed_n_bytes_in_range(monkeypatch, n_bytes, seed):
    monkeypatch.setattr(os, 'urandom', lambda n: "\x30" * n)

    gen_seed = generate_seed(n_bytes)
    assert gen_seed == seed


@pytest.mark.parametrize('n_bytes', [
    -1,
    0,
    257])
def test_generate_seed_n_bytes_out_range(n_bytes):
    with pytest.raises(ValueError):
        gen_seed = generate_seed(n_bytes)


def test_generate_seed_highest_bit(monkeypatch):
    monkeypatch.setattr(os, 'urandom', lambda n: "\x80" * n)

    gen_seed = generate_seed(4)
    assert gen_seed == 8421504
