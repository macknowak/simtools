# -*- coding: utf-8 -*-
"""Unit tests of miscellaneous utilities."""

import json

import pytest

from simtools.utils import save_versions


@pytest.fixture
def versions_dict():
    versions = {
        'model': '1.0',
        'mypackage': '1.2.3dev4'
        }
    return versions


def test_save_versions_dict(tmpdir, versions_dict):
    versions_file = tmpdir.join("versions_dict.json")

    save_versions(str(versions_file), versions_dict)
    versions_json = json.load(versions_file)
    for v in ('model', 'mypackage'):
        assert versions_json[v] == versions_dict[v]


@pytest.mark.parametrize('versions_filename, versions', [
    ("versions_tupletuple.json", (
        ('model', '1.0'),
        ('mypackage', '1.2.3dev4'))),
    ("versions_tuplelist.json", (
        ['model', '1.0'],
        ['mypackage', '1.2.3dev4'])),
    ("versions_listtuple.json", [
        ('model', '1.0'),
        ('mypackage', '1.2.3dev4')]),
    ("versions_listlist.json", [
        ['model', '1.0'],
        ['mypackage', '1.2.3dev4']])])
def test_save_versions_list_tuple(tmpdir, versions_filename, versions):
    versions_file = tmpdir.join(versions_filename)

    save_versions(str(versions_file), versions)
    versions_json = json.load(versions_file)
    for v, i in zip(('model', 'mypackage'), (0, 1)):
        assert versions_json[v] == versions[i][1]


@pytest.mark.parametrize('versions_filename, versions', [
    ("versions_nonnested", ('model', '1.0')),
    ("versions_toofew1", (
        ('model', '1.0'),
        'mypackage')),
    ("versions_toofew2", (
        ('model', '1.0'),
        ('mypackage', ))),
    ("versions_toomany", (
        ('model', '1.0'),
        ('mypackage', '1.2.3', 'dev4')))])
def test_save_versions_unpack(tmpdir, versions_filename, versions):
    versions_file = tmpdir.join(versions_filename)

    with pytest.raises(ValueError):
        save_versions(str(versions_file), versions)


def test_save_versions_indent(tmpdir, versions_dict):
    # Indent = 4
    versions_file = tmpdir.join("versions_indent4.json")

    save_versions(str(versions_file), versions_dict, indent=4)
    n_bytes4 = versions_file.size()
    n_lines4 = len(versions_file.readlines())
    assert n_lines4 == 4

    # Indent = 2
    versions_file = tmpdir.join("versions_indent2.json")

    save_versions(str(versions_file), versions_dict, indent=2)
    n_bytes2 = versions_file.size()
    assert n_bytes2 < n_bytes4
    n_lines2 = len(versions_file.readlines())
    assert n_lines2 == 4

    # Indent = None
    versions_file = tmpdir.join("versions_indentnone.json")

    save_versions(str(versions_file), versions_dict, indent=None)
    n_bytes_none = versions_file.size()
    assert n_bytes_none < n_bytes2
    n_lines_none = len(versions_file.readlines())
    assert n_lines_none == 1


@pytest.mark.parametrize('kwargs', [
    {'fp': None},
    {'obj': None}])
def test_save_versions_forbid_kwargs(tmpdir, versions_dict, kwargs):
    versions_file = tmpdir.join("versions_forbidkw.json")

    with pytest.raises(TypeError):
        save_versions(str(versions_file), versions_dict, **kwargs)
