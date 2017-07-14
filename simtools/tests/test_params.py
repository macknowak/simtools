# -*- coding: utf-8 -*-
"""Unit tests of parameter services."""

import pytest

from simtools.exceptions import ParamFileError
from simtools.params import Params


def test_params_load(tmpdir):
    # Correct
    params_file = tmpdir.join("params_ok.py")
    params_file.write(
"""p1 = 1
p2 = "abc"
p3 = {'a': 1, 'b': 2}
p4 = 1, 2, 3
p5 = [1, 2, 3]
p6 = [x+x for x in p5]
""")
    p = Params()

    p.load(str(params_file))
    assert p.p1 == 1
    assert p.p2 == "abc"
    assert p.p3 == {'a': 1, 'b': 2}
    assert p.p4 == (1, 2, 3)
    assert p.p5 == [1, 2, 3]
    assert p.p6 == [2, 4, 6]

    # Filename with no extension
    params_file = tmpdir.join("params_no_ext")
    p = Params()

    with pytest.raises(ValueError):
        p.load(str(params_file))

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
