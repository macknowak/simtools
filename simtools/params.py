# -*- coding: utf-8 -*-
"""Parameter services.

Parameter services provide the following functionality:

- loading parameters from a JSON file;
- loading parameters from a Python file;
- saving parameters to a JSON file;
- loading parameters from a file as a parameter set;
- saving parameter sets to a CSV file.
"""

import collections
import csv
import json
import sys
import types

from simtools.base import Dict
from simtools.exceptions import ParamFileError


class Params(Dict):
    """Container storing parameters."""

    def load(self, filename):
        """Load parameters from a file."""
        if filename.endswith(".json"):
            self._load_json(filename)
        elif filename.endswith(".py"):
            self._load_py(filename)
        else:
            raise ValueError("File format is not supported.")

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

    def _load_json(self, filename):
        """Load parameters from a JSON file."""
        with open(filename) as params_file:
            try:
                new_params = json.load(params_file)
            except ValueError as e:
                raise ParamFileError(filename=filename, error_msg=e.args[0])
            self.update(new_params)

    def _load_py(self, filename):
        """Load parameters from a Python file."""
        with open(filename) as params_file:
            # Execute Python code from the file to populate local namespace
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

            # Remove modules from the local namespace
            for paramname, paramval in new_params.items():
                if type(paramval) is types.ModuleType:
                    del new_params[paramname]

            # Update parameters
            self.update(new_params)


def load_params(filename):
    """Load parameters from a file."""
    params = Params()
    params.load(filename)
    return params


class ParamSets(collections.MutableSequence):
    """Container storing parameter sets."""

    def __init__(self):
        self._paramsets = []

    def __contains__(self, x):
        """Check if specific parameter set is stored."""
        return x in self._paramsets

    def __getitem__(self, index):
        """Retrieve parameter set at specific index."""
        return self._paramsets[index]

    def __setitem__(self, index, value):
        """Set parameter set at specific index."""
        if not isinstance(value, Params):
            raise TypeError("Type is not Params.")
        self._paramsets[index] = value

    def __delitem__(self, index):
        """Delete parameter set at specific index."""
        del self._paramsets[index]

    def __iter__(self):
        """Retrieve iterator over parameter sets."""
        return iter(self._paramsets)

    def __len__(self):
        """Retrieve number of parameter sets."""
        return len(self._paramsets)

    def __reversed__(self):
        """Retrieve reverse iterator over parameter sets."""
        return reversed(self._paramsets)

    def insert(self, index, value):
        """Insert parameter set before specific index."""
        if not isinstance(value, Params):
            raise TypeError("Type is not Params.")
        self._paramsets.insert(index, value)

    def load_params(self, filename):
        """Load parameters from a file as a parameter set."""
        self._paramsets.append(load_params(filename))

    def save(self, filename, paramnames, with_header=True, with_numbers=False,
             dialect='excel-tab'):
        """Save parameter sets to a file."""
        # Validate names of parameters to be saved
        try:
            iter(paramnames)
        except TypeError:
            raise TypeError("'paramnames' is not iterable.")
        try:
            basestring
        except NameError:
            basestring = str
        if isinstance(paramnames, basestring):
            raise TypeError("'paramnames' is a string.")
        for p, paramset in enumerate(self._paramsets):
            for paramname in paramnames:
                if paramname not in paramset:
                    raise ValueError("Selected parameter '{0}' is not found "
                                     "at index {1}.".format(paramname, p))

        # If necessary, create a field for record numbers
        if with_numbers:
            fieldnames = ['#']
            fieldnames.extend(paramnames)
        else:
            fieldnames = paramnames

        # Save parameter sets to a CSV file
        with open(filename, 'wb') as paramsets_file:
            csv_writer = csv.DictWriter(paramsets_file, fieldnames,
                                        extrasaction='ignore', dialect=dialect)
            if with_header:
                csv_writer.writeheader()
            for p, paramset in enumerate(self._paramsets):
                csv_row = paramset.copy()
                for paramname, paramval in csv_row.items():
                    # If parameter value is None, write it explicitly (by
                    # default, None is written as the empty string)
                    if paramval is None:
                        csv_row[paramname] = str(paramval)
                if with_numbers:
                    csv_row['#'] = p + 1
                csv_writer.writerow(csv_row)
