# -*- coding: utf-8 -*-
"""Unit tests of miscellaneous utilities."""

import json
import platform

import pytest

from simtools.utils import save_platform, save_versions


@pytest.fixture
def versions_dict():
    versions_info = {
        'model': '1.0',
        'mypackage': '1.2.3dev4'
        }
    return versions_info


def test_save_platform_default(tmpdir):
    platform_file = tmpdir.join("platform_default.json")

    save_platform(str(platform_file))
    platform_json = json.load(platform_file)
    platform_json['node'] == platform.node()
    platform_json['machine'] == platform.machine()
    platform_json['processor'] == platform.processor()
    platform_json['system'] == platform.system()
    platform_json['version'] == platform.version()
    platform_json['release'] == platform.release()


def test_save_platform_indent(tmpdir):
    # Indent = 4
    platform_file = tmpdir.join("platform_indent4.json")

    save_platform(str(platform_file), indent=4)
    n_bytes4 = platform_file.size()
    n_lines4 = len(platform_file.readlines())
    assert n_lines4 == 8

    # Indent = 2
    platform_file = tmpdir.join("platform_indent2.json")

    save_platform(str(platform_file), indent=2)
    n_bytes2 = platform_file.size()
    assert n_bytes2 < n_bytes4
    n_lines2 = len(platform_file.readlines())
    assert n_lines2 == 8

    # Indent = None
    platform_file = tmpdir.join("platform_indentnone.json")

    save_platform(str(platform_file), indent=None)
    n_bytes_none = platform_file.size()
    assert n_bytes_none < n_bytes2
    n_lines_none = len(platform_file.readlines())
    assert n_lines_none == 1


@pytest.mark.parametrize('kwargs', [
    {'fp': None},
    {'obj': None}])
def test_save_platform_forbid_kwargs(tmpdir, kwargs):
    platform_file = tmpdir.join("platform_forbidkw.json")

    with pytest.raises(TypeError):
        save_platform(str(platform_file), **kwargs)


def test_save_versions_dict(tmpdir, versions_dict):
    versions_file = tmpdir.join("versions_dict.json")

    save_versions(str(versions_file), versions_dict)
    versions_json = json.load(versions_file)
    for v in ('model', 'mypackage'):
        assert versions_json[v] == versions_dict[v]


@pytest.mark.parametrize('versions_filename, versions_info', [
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
def test_save_versions_list_tuple(tmpdir, versions_filename, versions_info):
    versions_file = tmpdir.join(versions_filename)

    save_versions(str(versions_file), versions_info)
    versions_json = json.load(versions_file)
    for v, i in zip(('model', 'mypackage'), (0, 1)):
        assert versions_json[v] == versions_info[i][1]


@pytest.mark.parametrize('versions_filename, versions_info', [
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
def test_save_versions_unpack(tmpdir, versions_filename, versions_info):
    versions_file = tmpdir.join(versions_filename)

    with pytest.raises(ValueError):
        save_versions(str(versions_file), versions_info)


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
