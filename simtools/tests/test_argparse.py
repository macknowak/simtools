# -*- coding: utf-8 -*-
"""Unit tests of command line argument parsing services."""

import os
import sys

import pytest

from simtools.argparse import parse_args


@pytest.mark.parametrize('argv', [
    ["model.py", "-p", "params.py", "-i", "20001020_102030", "-s", "-d", "."],
    ["model.py", "--params", "params.py", "--simid", "20001020_102030",
     "--save", "--data-dir", "."]])
def test_run_options(monkeypatch, tmpdir, argv):
    tmpdir.join("params.py").write("")
    monkeypatch.setattr(sys, 'argv', argv)

    with tmpdir.as_cwd():
        # Only selected options
        allow_options = ['params_filename', 'sim_id', 'save_data',
                         'data_dirname']

        options = parse_args(allow_options)
        assert options.params_filename == "params.py"
        assert options.sim_id == "20001020_102030"
        assert options.save_data == True
        with pytest.raises(AttributeError):
            options.only_test_params

        # All supported options
        allow_options = ['params_filename', 'sim_id', 'save_data',
                         'data_dirname', 'only_test_params']

        options = parse_args(allow_options)
        assert options.params_filename == "params.py"
        assert options.sim_id == "20001020_102030"
        assert options.save_data == True
        assert options.only_test_params == False


@pytest.mark.parametrize('argv', [
    ["model.py", "-p", "params.py", "-t"],
    ["model.py", "--params", "params.py", "--only-params"]])
def test_only_test_params_option(monkeypatch, tmpdir, argv):
    tmpdir.join("params.py").write("")
    monkeypatch.setattr(sys, 'argv', argv)

    with tmpdir.as_cwd():
        # Only selected options
        allow_options = ['params_filename', 'only_test_params']

        options = parse_args(allow_options)
        assert options.params_filename == "params.py"
        with pytest.raises(AttributeError):
            options.sim_id
        with pytest.raises(AttributeError):
            options.save_data
        assert options.only_test_params == True

        # All supported options
        allow_options = ['params_filename', 'sim_id', 'save_data',
                         'data_dirname', 'only_test_params']

        options = parse_args(allow_options)
        assert options.params_filename == "params.py"
        assert options.sim_id == None
        assert options.save_data == False
        assert options.only_test_params == True


def test_params_filename_option(monkeypatch, tmpdir):
    allow_options = ['params_filename']

    # Correct
    params_file = tmpdir.join("params.py")
    params_file.write("")
    argv = ["model.py", "-p", str(params_file)]
    monkeypatch.setattr(sys, 'argv', argv)

    options = parse_args(allow_options)
    assert options.params_filename == str(params_file)

    # Non-existing parameter file
    params_file = tmpdir.join("nonexist.py")
    argv = ["model.py", "-p", str(params_file)]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options = parse_args(allow_options)

    # Existing parameter file with no access
    params_file = tmpdir.join("noaccess.py")
    params_file.write("")
    os.chmod(str(params_file), 0)
    argv = ["model.py", "-p", str(params_file)]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options = parse_args(allow_options)


def test_data_dirname_option(monkeypatch, tmpdir):
    allow_options = ['data_dirname']

    # Correct
    datadir = tmpdir.mkdir("data")
    argv = ["model.py", "-d", str(datadir)]
    monkeypatch.setattr(sys, 'argv', argv)

    options = parse_args(allow_options)
    assert options.data_dirname == str(datadir)

    # Non-existing directory
    datadir = tmpdir.join("nonexist")
    argv = ["model.py", "-d", str(datadir)]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options = parse_args(allow_options)

    # Existing directory with no access
    datadir = tmpdir.mkdir("noaccess")
    os.chmod(str(datadir), 0)
    argv = ["model.py", "-d", str(datadir)]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options = parse_args(allow_options)


@pytest.mark.parametrize('allow_options', [
    ['unsupported'],
    ['params_filename', 'sim_id', 'save_data', 'only_test_params',
     'unsupported']])
def test_unsupported_option(monkeypatch, allow_options):
    argv = ["model.py", "--unsupported"]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options = parse_args(allow_options)


def test_unrecognized_args(monkeypatch):
    # Option supported, but not allowed
    argv = ["model.py", "-t"]
    monkeypatch.setattr(sys, 'argv', argv)
    allow_options = ['params_filename', 'sim_id', 'save_data']

    with pytest.raises(SystemExit):
        options = parse_args(allow_options)

    # Unsupported argument
    argv = ["model.py", "--unsupported"]
    monkeypatch.setattr(sys, 'argv', argv)
    allow_options = ['params_filename', 'sim_id', 'save_data',
                     'only_test_params']

    with pytest.raises(SystemExit):
        options = parse_args(allow_options)
