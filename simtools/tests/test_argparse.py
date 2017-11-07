# -*- coding: utf-8 -*-
"""Unit tests of command line argument parsing services."""

import os
import sys

import pytest

from simtools.argparse import parse_args, parse_known_args


@pytest.mark.parametrize('argv', [
    ["model.py", "-p", "params.py", "-i", "20001020_102030", "-s", "-d", "."],
    ["model.py", "--params", "params.py", "--simid", "20001020_102030",
     "--save", "--data-dir", "."]])
def test_parse_args_run_options(monkeypatch, tmpdir, argv):
    tmpdir.join("params.py").write("")
    monkeypatch.setattr(sys, 'argv', argv)

    with tmpdir.as_cwd():
        # Only selected options
        allowed_options = ['params_filename', 'sim_id', 'save_data',
                           'data_dirname']

        options = parse_args(allowed_options)
        assert options.params_filename == "params.py"
        assert options.sim_id == "20001020_102030"
        assert options.save_data == True
        with pytest.raises(AttributeError):
            options.only_test_params

        # All supported options
        allowed_options = ['params_filename', 'sim_id', 'save_data',
                           'data_dirname', 'only_test_params']

        options = parse_args(allowed_options)
        assert options.params_filename == "params.py"
        assert options.sim_id == "20001020_102030"
        assert options.save_data == True
        assert options.only_test_params == False


@pytest.mark.parametrize('argv', [
    ["model.py", "-p", "params.py", "-t"],
    ["model.py", "--params", "params.py", "--only-params"]])
def test_parse_args_only_test_params_option(monkeypatch, tmpdir, argv):
    tmpdir.join("params.py").write("")
    monkeypatch.setattr(sys, 'argv', argv)

    with tmpdir.as_cwd():
        # Only selected options
        allowed_options = ['params_filename', 'only_test_params']

        options = parse_args(allowed_options)
        assert options.params_filename == "params.py"
        with pytest.raises(AttributeError):
            options.sim_id
        with pytest.raises(AttributeError):
            options.save_data
        assert options.only_test_params == True

        # All supported options
        allowed_options = ['params_filename', 'sim_id', 'save_data',
                           'data_dirname', 'only_test_params']

        options = parse_args(allowed_options)
        assert options.params_filename == "params.py"
        assert options.sim_id == None
        assert options.save_data == False
        assert options.only_test_params == True


def test_parse_args_params_filename_option(monkeypatch, tmpdir):
    allowed_options = ['params_filename']

    # Correct
    params_file = tmpdir.join("params.py")
    params_file.write("")
    argv = ["model.py", "-p", str(params_file)]
    monkeypatch.setattr(sys, 'argv', argv)

    options = parse_args(allowed_options)
    assert options.params_filename == str(params_file)

    # Non-existing parameter file
    params_file = tmpdir.join("nonexist.py")
    argv = ["model.py", "-p", str(params_file)]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options = parse_args(allowed_options)

    # Existing parameter file with no access
    params_file = tmpdir.join("noaccess.py")
    params_file.write("")
    os.chmod(str(params_file), 0)
    argv = ["model.py", "-p", str(params_file)]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options = parse_args(allowed_options)


def test_parse_args_data_dirname_option(monkeypatch, tmpdir):
    allowed_options = ['data_dirname']

    # Correct
    datadir = tmpdir.mkdir("data")
    argv = ["model.py", "-d", str(datadir)]
    monkeypatch.setattr(sys, 'argv', argv)

    options = parse_args(allowed_options)
    assert options.data_dirname == str(datadir)

    # Non-existing directory
    datadir = tmpdir.join("nonexist")
    argv = ["model.py", "-d", str(datadir)]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options = parse_args(allowed_options)

    # Existing directory with no access
    datadir = tmpdir.mkdir("noaccess")
    os.chmod(str(datadir), 0)
    argv = ["model.py", "-d", str(datadir)]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options = parse_args(allowed_options)


@pytest.mark.parametrize('argv', [
    ["model.py", "-i", "20001020_102030", "-s"],
    ["model.py", "-t"]])
def test_parse_args_disallowed_option(monkeypatch, argv):
    monkeypatch.setattr(sys, 'argv', argv)
    allowed_options = ['save_data']

    with pytest.raises(SystemExit):
        options = parse_args(allowed_options)


@pytest.mark.parametrize('allowed_options', [
    ['unsupported'],
    ['params_filename', 'sim_id', 'save_data', 'only_test_params',
     'unsupported']])
def test_parse_args_unsupported_option(monkeypatch, allowed_options):
    argv = ["model.py", "--unsupported"]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options = parse_args(allowed_options)


@pytest.mark.parametrize('argv', [
    ["model.py", "-x", "1.5", "-y", "0", "-i", "20001020_102030",
     "--transform", "scale", "-s", "-v"],
    ["model.py", "-x", "1.5", "-y", "0", "--transform", "scale", "-v"]])
def test_parse_args_extra_args(monkeypatch, argv):
    monkeypatch.setattr(sys, 'argv', argv)
    allowed_options = ['sim_id', 'data_dirname', 'save_data']

    with pytest.raises(SystemExit):
        options = parse_args(allowed_options)


@pytest.mark.parametrize('argv', [
    ["model.py", "-p", "params.py", "-i", "20001020_102030", "-s", "-d", "."],
    ["model.py", "--params", "params.py", "--simid", "20001020_102030",
     "--save", "--data-dir", "."]])
def test_parse_known_args_run_options(monkeypatch, tmpdir, argv):
    tmpdir.join("params.py").write("")
    monkeypatch.setattr(sys, 'argv', argv)

    with tmpdir.as_cwd():
        # Only selected options
        allowed_options = ['params_filename', 'sim_id', 'save_data',
                           'data_dirname']

        options, extra_args = parse_known_args(allowed_options)
        assert options.params_filename == "params.py"
        assert options.sim_id == "20001020_102030"
        assert options.save_data == True
        with pytest.raises(AttributeError):
            options.only_test_params
        assert extra_args == []

        # All supported options
        allowed_options = ['params_filename', 'sim_id', 'save_data',
                           'data_dirname', 'only_test_params']

        options, extra_args = parse_known_args(allowed_options)
        assert options.params_filename == "params.py"
        assert options.sim_id == "20001020_102030"
        assert options.save_data == True
        assert options.only_test_params == False
        assert extra_args == []


@pytest.mark.parametrize('argv', [
    ["model.py", "-p", "params.py", "-t"],
    ["model.py", "--params", "params.py", "--only-params"]])
def test_parse_known_args_only_test_params_option(monkeypatch, tmpdir, argv):
    tmpdir.join("params.py").write("")
    monkeypatch.setattr(sys, 'argv', argv)

    with tmpdir.as_cwd():
        # Only selected options
        allowed_options = ['params_filename', 'only_test_params']

        options, extra_args = parse_known_args(allowed_options)
        assert options.params_filename == "params.py"
        with pytest.raises(AttributeError):
            options.sim_id
        with pytest.raises(AttributeError):
            options.save_data
        assert options.only_test_params == True
        assert extra_args == []

        # All supported options
        allowed_options = ['params_filename', 'sim_id', 'save_data',
                           'data_dirname', 'only_test_params']

        options, extra_args = parse_known_args(allowed_options)
        assert options.params_filename == "params.py"
        assert options.sim_id == None
        assert options.save_data == False
        assert options.only_test_params == True
        assert extra_args == []


def test_parse_known_args_params_filename_option(monkeypatch, tmpdir):
    allowed_options = ['params_filename']

    # Correct
    params_file = tmpdir.join("params.py")
    params_file.write("")
    argv = ["model.py", "-p", str(params_file)]
    monkeypatch.setattr(sys, 'argv', argv)

    options, extra_args = parse_known_args(allowed_options)
    assert options.params_filename == str(params_file)

    # Non-existing parameter file
    params_file = tmpdir.join("nonexist.py")
    argv = ["model.py", "-p", str(params_file)]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options, extra_args = parse_known_args(allowed_options)

    # Existing parameter file with no access
    params_file = tmpdir.join("noaccess.py")
    params_file.write("")
    os.chmod(str(params_file), 0)
    argv = ["model.py", "-p", str(params_file)]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options, extra_args = parse_known_args(allowed_options)


def test_parse_known_args_data_dirname_option(monkeypatch, tmpdir):
    allowed_options = ['data_dirname']

    # Correct
    datadir = tmpdir.mkdir("data")
    argv = ["model.py", "-d", str(datadir)]
    monkeypatch.setattr(sys, 'argv', argv)

    options, extra_args = parse_known_args(allowed_options)
    assert options.data_dirname == str(datadir)

    # Non-existing directory
    datadir = tmpdir.join("nonexist")
    argv = ["model.py", "-d", str(datadir)]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options, extra_args = parse_known_args(allowed_options)

    # Existing directory with no access
    datadir = tmpdir.mkdir("noaccess")
    os.chmod(str(datadir), 0)
    argv = ["model.py", "-d", str(datadir)]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options, extra_args = parse_known_args(allowed_options)


def test_parse_known_args_disallowed_option(monkeypatch):
    allowed_options = ['save_data']

    # Mixed allowed and disallowed options
    argv = ["model.py", "-i", "20001020_102030", "-s"]
    monkeypatch.setattr(sys, 'argv', argv)

    options, extra_args = parse_known_args(allowed_options)
    assert options.save_data == True
    assert extra_args == ["-i", "20001020_102030"]

    # Only disallowed option
    argv = ["model.py", "-t"]
    monkeypatch.setattr(sys, 'argv', argv)

    options, extra_args = parse_known_args(allowed_options)
    assert options.save_data == False
    assert extra_args == ["-t"]


@pytest.mark.parametrize('allowed_options', [
    ['unsupported'],
    ['params_filename', 'sim_id', 'save_data', 'only_test_params',
     'unsupported']])
def test_parse_known_args_unsupported_option(monkeypatch, allowed_options):
    argv = ["model.py", "--unsupported"]
    monkeypatch.setattr(sys, 'argv', argv)

    with pytest.raises(SystemExit):
        options, extra_args = parse_known_args(allowed_options)


def test_parse_known_args_extra_args(monkeypatch):
    allowed_options = ['sim_id', 'data_dirname', 'save_data']

    # Mixed allowed options and extra arguments
    argv = ["model.py", "-x", "1.5", "-y", "0", "-i", "20001020_102030",
            "--transform", "scale", "-s", "-v"]
    monkeypatch.setattr(sys, 'argv', argv)

    options, extra_args = parse_known_args(allowed_options)
    with pytest.raises(AttributeError):
        options.params_filename
    assert options.sim_id == "20001020_102030"
    assert options.data_dirname is None
    assert options.save_data == True
    with pytest.raises(AttributeError):
        options.only_test_params
    assert extra_args == [argv[a] for a in (1, 2, 3, 4, 7, 8, 10)]

    # Only extra arguments
    argv = ["model.py", "-x", "1.5", "-y", "0", "--transform", "scale", "-v"]
    monkeypatch.setattr(sys, 'argv', argv)

    options, extra_args = parse_known_args(allowed_options)
    with pytest.raises(AttributeError):
        options.params_filename
    assert options.sim_id is None
    assert options.data_dirname is None
    assert options.save_data == False
    with pytest.raises(AttributeError):
        options.only_test_params
    assert extra_args == argv[1:]
