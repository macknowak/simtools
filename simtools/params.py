# -*- coding: utf-8 -*-
"""Parameter services.

Parameter services provide the following functionality:

- loading parameters from a JSON file;
- loading parameters from a Python file;
- saving parameters to a JSON file;
- loading parameters from a file as a parameter set;
- saving parameter sets to a CSV file;
- saving parameter sets to a JSON file;
- exporting parameters of multiple simulations to a file;
- loading parameter names from a text file.
"""

import csv
import json
import sys
import types

from simtools.base import Dict, is_iterable, is_string
from simtools.exceptions import FileError

if sys.version_info[0] == 3:
    import collections.abc as collections_abc
else:
    import collections as collections_abc


class Params(Dict):
    """Container storing parameters."""

    def load(self, filename):
        """Load parameters from a file."""
        filename_lower = filename.lower()
        if filename_lower.endswith(".json"):
            self._load_json(filename)
        elif filename_lower.endswith(".py"):
            self._load_py(filename)
        else:
            raise ValueError("File format is not supported.")

    def save(self, filename, paramnames=None, **kwargs):
        """Save parameters to a file."""
        DEFAULT_INDENT = 4

        # If necessary, validate names of parameters to be saved
        if paramnames is not None:
            if not is_iterable(paramnames):
                raise TypeError("'paramnames' is not iterable.")
            if is_string(paramnames):
                raise TypeError("'paramnames' is a string.")
            if len(paramnames) > len(set(paramnames)):
                raise ValueError("'paramnames' contains duplicate values.")

        # If necessary, validate extra keyword arguments
        if kwargs:
            for arg in ('obj', 'fp'):
                if arg in kwargs:
                    raise TypeError("save() got an unexpected keyword "
                                    "argument '{}'.".format(arg))

        # Determine parameters to be saved
        if paramnames is not None:
            try:
                params = {p: self[p] for p in paramnames}
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
                raise FileError(filename=filename, error_msg=e.args[0])
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
                raise FileError(filename=filename, lineno=lineno,
                                error_msg=exc_value.args[0])

            # Remove modules from the local namespace
            for paramname, paramval in list(new_params.items()):
                if type(paramval) is types.ModuleType:
                    del new_params[paramname]

            # Update parameters
            self.update(new_params)


class ParamSets(collections_abc.MutableSequence):
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

    def save(self, filename, paramnames, paramnames_map=None,
             with_numbers=False, **kwargs):
        """Save parameter sets to a file."""
        # Validate names of parameters to be saved
        if not is_iterable(paramnames):
            raise TypeError("'paramnames' is not iterable.")
        if is_string(paramnames):
            raise TypeError("'paramnames' is a string.")
        if len(paramnames) > len(set(paramnames)):
            raise ValueError("'paramnames' contains duplicate values.")

        # Save parameter sets to a file according to the file extension
        filename_lower = filename.lower()
        if filename_lower.endswith(".csv"):
            self._save_csv(filename, paramnames, paramnames_map, with_numbers,
                           **kwargs)
        elif filename_lower.endswith(".json"):
            self._save_json(filename, paramnames, paramnames_map, with_numbers,
                            **kwargs)
        else:
            raise ValueError("File format is not supported.")

    def _make_records(self, paramnames, record_paramnames, with_numbers,
                      explicit_none):
        """Create parameter records for saving to a file."""
        params_records = []
        for p, paramset in enumerate(self._paramsets):
            # Populate parameter record corresponding to the parameter set
            params_record = {}
            for paramname, record_paramname in zip(paramnames,
                                                   record_paramnames):
                # Evaluate parameter
                try:
                    paramval = eval(paramname, globals(), paramset)
                except Exception:
                    raise ValueError("Selected parameter '{0}' is not found "
                                     "at index {1}.".format(paramname, p))

                # If necessary, if parameter value is None, write it explicitly
                # (by default, None is written as the empty string), otherwise
                # use the value itself
                if explicit_none and paramval is None:
                    params_record[record_paramname] = str(paramval)
                else:
                    params_record[record_paramname] = paramval

            # If necessary, determine record number
            if with_numbers:
                params_record['#'] = p + 1

            params_records.append(params_record)

        return params_records

    def _save_csv(self, filename, paramnames, paramnames_map, with_numbers,
                  with_header=True, dialect='excel-tab'):
        """Save parameter sets to a CSV file."""
        # Determine parameter names in parameter records
        record_paramnames = self._substitute_paramnames(paramnames,
                                                        paramnames_map)

        # Determine parameter records to be saved
        params_records = self._make_records(paramnames, record_paramnames,
                                            with_numbers, explicit_none=True)

        # Determine field names
        if with_numbers:
            fieldnames = ['#']
            fieldnames.extend(record_paramnames)
        else:
            fieldnames = record_paramnames

        # Save parameter records to a CSV file
        if sys.version_info[0] == 3:
            paramsets_file = open(filename, 'w', newline='')
        else:
            paramsets_file = open(filename, 'wb')
        with paramsets_file:
            csv_writer = csv.DictWriter(paramsets_file, fieldnames,
                                        extrasaction='ignore', dialect=dialect)
            if with_header:
                csv_writer.writeheader()
            csv_writer.writerows(params_records)

    def _save_json(self, filename, paramnames, paramnames_map, with_numbers,
                   **kwargs):
        """Save parameter sets to a JSON file."""
        DEFAULT_INDENT = 4

        # If necessary, validate extra keyword arguments
        if kwargs:
            for arg in ('obj', 'fp'):
                if arg in kwargs:
                    raise TypeError("_save_json() got an unexpected keyword "
                                    "argument '{}'.".format(arg))

        # Determine parameter names in parameter records
        record_paramnames = self._substitute_paramnames(paramnames,
                                                        paramnames_map)

        # Determine parameter records to be saved
        params_records = self._make_records(paramnames, record_paramnames,
                                            with_numbers, explicit_none=False)

        # Determine indentation
        indent = kwargs.pop('indent', DEFAULT_INDENT)

        # Save parameter records to a JSON file
        with open(filename, 'w') as paramsets_file:
            json.dump(params_records, paramsets_file, indent=indent, **kwargs)

    def _substitute_paramnames(self, paramnames, paramnames_map):
        """Substitute parameter names according to a mapping."""
        # If no mapping of parameter names is provided, do not substitute
        # parameter names
        if paramnames_map is None:
            return paramnames

        # Validate mapping of parameter names
        for paramname in paramnames_map.keys():
            if paramname not in paramnames:
                raise ValueError(
                    "Key '{}' in 'paramnames_map' is not a parameter name "
                    "in 'paramnames'.".format(paramname))

        # Determine substituted parameter names
        new_paramnames = [paramname if paramname not in paramnames_map
                          else paramnames_map[paramname]
                          for paramname in paramnames]
        if len(set(new_paramnames)) < len(paramnames):
            raise ValueError("Substituted parameter names are not unique.")

        return new_paramnames


def load_params(filename):
    """Load parameters from a file."""
    params = Params()
    params.load(filename)
    return params


def export_params(export_filename, params_paths, paramnames,
                  paramnames_map=None, with_numbers=False, **kwargs):
    """Export parameters of multiple simulations to a file."""
    # Validate export filename extension
    if not any(map(export_filename.lower().endswith, (".csv", ".json"))):
        raise ValueError("File format is not supported.")

    # Load parameters from parameter files as parameter sets
    paramsets = ParamSets()
    for params_path in params_paths:
        paramsets.load_params(params_path)

    # Save parameter sets to the export file
    paramsets.save(export_filename, paramnames, paramnames_map, with_numbers,
                   **kwargs)


def load_paramnames(filename, full_paramnames_map=False):
    """Load parameter names from a file."""
    COMMENT_START_TOKEN = "#"
    PARAMNAME_SUBSTITUTION_TOKEN = "->"

    paramnames = []
    paramnames_map = {}
    lineno = 0
    with open(filename) as paramnames_file:
        for line in paramnames_file:
            # Increment the line number and strip leading and trailing
            # whitespace from the line
            lineno += 1
            stripped_line = line.strip()

            # If the stripped line is empty or contains only a comment, skip it
            if (not stripped_line
                or stripped_line.startswith(COMMENT_START_TOKEN)):
                continue

            # Assume that the stripped line contains either a single parameter
            # name or two parameter names separated by a substitution symbol
            # and extract them
            line_parts = stripped_line.split(PARAMNAME_SUBSTITUTION_TOKEN)
            n_line_parts = len(line_parts)
            if n_line_parts == 1:  # single parameter name
                paramname = line_parts[0]
                paramnames.append(paramname)
                if full_paramnames_map:
                    paramnames_map[paramname] = paramname
            elif n_line_parts == 2:  # two parameter names: original and
                                     # substituted
                paramname = line_parts[0].rstrip()
                new_paramname = line_parts[1].lstrip()
                paramnames.append(paramname)
                paramnames_map[paramname] = new_paramname
            else:
                raise FileError(filename=filename, lineno=lineno,
                                error_msg="invalid syntax", line=line)
    return paramnames, paramnames_map
