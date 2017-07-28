# -*- coding: utf-8 -*-
"""Parameter services.

Parameter services provide the following functionality:

- loading parameters from a Python file;
- saving parameters to a JSON file.
"""

import json
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

    def save(self, filename, save_params=None, **kwargs):
        """Save parameters to a file."""
        DEFAULT_INDENT = 4

        # If necessary, validate parameters to be saved
        if save_params is not None:
            try:
                iter(save_params)
            except TypeError:
                raise TypeError("'save_params' is not iterable.")
            try:
                basestring
            except NameError:
                basestring = str
            if isinstance(save_params, basestring):
                raise TypeError("'save_params' is a string.")

        # If necessary, validate extra keyword arguments
        if kwargs:
            for arg in ('obj', 'fp'):
                if arg in kwargs:
                    raise TypeError("save() got an unexpected keyword "
                                    "argument '{}'.".format(arg))

        # Determine parameters to be saved
        if save_params is not None:
            try:
                params = {p: self[p] for p in save_params}
            except KeyError as e:
                raise ValueError(
                    "Selected parameter '{}' is not found.".format(e.args[0]))
        else:
            params = self

        # Determine indentation
        indent = kwargs.pop('indent', DEFAULT_INDENT)

        # Save parameters to a JSON file
        with open(filename, 'w') as params_file:
            json.dump(params, params_file, indent=indent, **kwargs)


def load_params(filename):
    """Load parameters from a file."""
    params = Params()
    params.load(filename)
    return params
