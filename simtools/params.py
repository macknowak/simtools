# -*- coding: utf-8 -*-
"""Parameter services.

Parameter services provide loading parameters from a Python file.
"""

import sys

from simtools.base import Dict
from simtools.exceptions import ParamFileError


class Params(Dict):
    """Container storing parameters."""

    def load(self, filename):
        """Load parameters from a file."""
        # Check if the file format represents Python code
        if not filename.endswith(".py"):
            raise ValueError("File format is not supported.")

        # Execute Python code from the file and update parameters accordingly
        with open(filename) as params_file:
            new_params = {}
            try:
                exec(params_file.read(), globals(), new_params)
            except Exception:
                _, exc_value, exc_traceback = sys.exc_info()
                lineno = (exc_traceback.tb_next.tb_lineno
                          if hasattr(exc_traceback.tb_next, 'tb_lineno')
                          else None)
                del exc_traceback
                raise ParamFileError(filename=filename, lineno=lineno,
                                     error_msg=exc_value.args[0])
            self.update(new_params)


def load_params(filename):
    """Load parameters from a file."""
    params = Params()
    params.load(filename)
    return params
