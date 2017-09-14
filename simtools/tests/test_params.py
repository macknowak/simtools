# -*- coding: utf-8 -*-
"""Unit tests of parameter services."""

import json
import math

import pytest

from simtools.exceptions import ParamFileError
from simtools.params import ParamSets, Params


@pytest.fixture
def params():
    p = Params()
    p.p1 = 1
    p.p2 = 2.5
    p.p3 = math.pi
    p.p4 = "abc"
    p.p5 = {'a': 1, 'b': 2.5, 'c': math.pi, 'd': "abc"}
    p.p6 = 1, 2.5, math.pi, "abc"
    p.p7 = [1, 2.5, math.pi, "abc"]
    return p


def test_params_load_json(tmpdir):
    # Correct
    params_file = tmpdir.join("params_ok.json")
    params_file.write(
"""{
    "p1": 1,
    "p2": 2.5,
    "p3": 3.141592653589793,
    "p4": "abc",
    "p5": {
        "a": 1,
        "b": 2.5,
        "c": 3.141592653589793,
        "d": "abc"
    },
    "p6": [
        1,
        2.5,
        3.141592653589793,
        "abc"
    ]
}""")
    p = Params()

    p.load(str(params_file))
    assert p.p1 == 1
    assert p.p2 == 2.5
    assert p.p3 == math.pi
    assert p.p4 == "abc"
    assert p.p5 == {'a': 1, 'b': 2.5, 'c': math.pi, 'd': "abc"}
    assert p.p6 == [1, 2.5, math.pi, "abc"]

    # Syntax error
    params_file = tmpdir.join("params_syntax.json")
    params_file.write(
"""\"p1": 1,
"p2": 2.5,
"p3": 3.141592653589793,
"p4": "abc",
"p5": {
    "a": 1,
    "b": 2.5,
    "c": 3.141592653589793,
    "d": "abc"
},
"p6": [
    1,
    2.5,
    3.141592653589793,
    "abc"
]""")
    p = Params()

    with pytest.raises(ParamFileError):
        p.load(str(params_file))


def test_params_load_py(tmpdir):
    # Correct
    params_file = tmpdir.join("params_ok.py")
    params_file.write(
"""import math

p1 = 1
p2 = 2.5
p3 = math.pi
p4 = "abc"
p5 = {'a': 1, 'b': 2.5, 'c': math.pi, 'd': "abc"}
p6 = 1, 2.5, math.pi, "abc"
p7 = [1, 2.5, math.pi, "abc"]
p8 = [x+x for x in [1, 2, 3]]  # list comprehension
""")
    p = Params()

    p.load(str(params_file))
    assert p.p1 == 1
    assert p.p2 == 2.5
    assert p.p3 == math.pi
    assert p.p4 == "abc"
    assert p.p5 == {'a': 1, 'b': 2.5, 'c': math.pi, 'd': "abc"}
    assert p.p6 == (1, 2.5, math.pi, "abc")
    assert p.p7 == [1, 2.5, math.pi, "abc"]
    assert p.p8 == [2, 4, 6]
    with pytest.raises(AttributeError):
        p.math

    # Syntax error
    params_file = tmpdir.join("params_syntax.py")
    params_file.write(
"""p1 = 5
p2 = [x+x for x in]
""")
    p = Params()

    with pytest.raises(ParamFileError):
        p.load(str(params_file))

    # Division by 0
    params_file = tmpdir.join("params_div_zero.py")
    params_file.write(
"""p1 = 5
p2 = 5 / 0
""")
    p = Params()

    with pytest.raises(ParamFileError):
        p.load(str(params_file))

    # Undefined name
    params_file = tmpdir.join("params_undef_name.py")
    params_file.write(
"""p1 = 5
p2
""")
    p = Params()

    with pytest.raises(ParamFileError):
        p.load(str(params_file))


def test_params_load_no_ext(tmpdir):
    params_file = tmpdir.join("params_no_ext")
    p = Params()

    with pytest.raises(ValueError):
        p.load(str(params_file))


def test_params_save_default(tmpdir, params):
    params_file = tmpdir.join("params_default.json")

    params.save(str(params_file))
    params_json = json.load(params_file)
    for p in ('p1', 'p2', 'p3', 'p4', 'p5', 'p7'):
        assert params_json[p] == params[p]
    assert params_json['p6'] == list(params['p6'])


def test_params_save_save_params(tmpdir, params):
    # All parameters
    params_file = tmpdir.join("params_all.json")
    save_params = ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']

    params.save(str(params_file), save_params)
    params_json = json.load(params_file)
    for p in ('p1', 'p2', 'p3', 'p4', 'p5', 'p7'):
        assert params_json[p] == params[p]
    assert params_json['p6'] == list(params['p6'])

    # Some parameters
    params_file = tmpdir.join("params_some.json")
    save_params = ['p1', 'p4', 'p7']

    params.save(str(params_file), save_params)
    params_json = json.load(params_file)
    for p in ('p1', 'p4', 'p7'):
        assert params_json[p] == params[p]
    for p in ('p2', 'p3', 'p5', 'p6'):
        with pytest.raises(KeyError):
            assert params_json[p] == params[p]

    # Not iterable
    params_file = tmpdir.join("params_notiter.json")
    save_params = 1

    with pytest.raises(TypeError):
        params.save(str(params_file), save_params)

    # String
    params_file = tmpdir.join("params_string.json")
    save_params = "p1, p2, p3, p4, p5, p6, p7"

    with pytest.raises(TypeError):
        params.save(str(params_file), save_params)

    # Non-existing parameter
    params_file = tmpdir.join("params_nonexist.json")
    save_params = ['p1', 'p999']

    with pytest.raises(ValueError):
        params.save(str(params_file), save_params)


def test_params_save_indent(tmpdir, params):
    # Indent = 4
    params_file = tmpdir.join("params_indent4.json")

    params.save(str(params_file), indent=4)
    n_bytes4 = params_file.size()
    n_lines4 = len(params_file.readlines())
    assert n_lines4 == 24

    # Indent = 2
    params_file = tmpdir.join("params_indent2.json")

    params.save(str(params_file), indent=2)
    n_bytes2 = params_file.size()
    assert n_bytes2 < n_bytes4
    n_lines2 = len(params_file.readlines())
    assert n_lines2 == 24

    # Indent = None
    params_file = tmpdir.join("params_indentnone.json")

    params.save(str(params_file), indent=None)
    n_bytes_none = params_file.size()
    assert n_bytes_none < n_bytes2
    n_lines_none = len(params_file.readlines())
    assert n_lines_none == 1


@pytest.mark.parametrize('kwargs', [
    {'fp': None},
    {'obj': None}])
def test_params_save_forbid_kwargs(tmpdir, params, kwargs):
    params_file = tmpdir.join("params_forbidkw.json")

    with pytest.raises(TypeError):
        params.save(str(params_file), **kwargs)


def test_paramsets_empty():
    paramsets = ParamSets()
    assert len(paramsets) == 0
    with pytest.raises(IndexError):
        paramsets[0]
    with pytest.raises(StopIteration):
        iter(paramsets).next()
    with pytest.raises(StopIteration):
        reversed(paramsets).next()


def test_paramsets_load_params(tmpdir):
    params_file_json = tmpdir.join("params.json")
    params_file_json.write(
"""{
    "p1": 1,
    "p2": 2.5,
    "p3": "abc"
}""")
    params_file_py = tmpdir.join("params.py")
    params_file_py.write(
"""p1 = 1
p2 = 2.5
p3 = "abc"
""")
    paramsets = ParamSets()

    # First parameter set (from a JSON file)
    paramsets.load_params(str(params_file_json))
    assert len(paramsets) == 1
    assert paramsets[0].p1 == 1
    assert paramsets[0].p2 == 2.5
    assert paramsets[0].p3 == "abc"
    with pytest.raises(IndexError):
        paramsets[1]

    # Second parameter set (from a Python file)
    paramsets.load_params(str(params_file_py))
    assert len(paramsets) == 2
    assert paramsets[1].p1 == 1
    assert paramsets[1].p2 == 2.5
    assert paramsets[1].p3 == "abc"
    with pytest.raises(IndexError):
        paramsets[2]
