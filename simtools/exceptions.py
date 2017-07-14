# -*- coding: utf-8 -*-
"""Exceptions and warnings raised by SimTools.

Exceptions include:

- ParamFileError - raised during processing a parameter file.
"""


class SimToolsError(Exception):
    """Base SimTools exception."""
    pass


class ParamFileError(SimToolsError):
    """Error during processing a parameter file."""

    def __init__(self, msg="", filename=None, lineno=None, error_msg=None):
        if not msg and any((filename, lineno, error_msg)):
            if filename:
                msg = "File '{}' is invalid".format(filename)
            else:
                msg = "File is invalid"
            if lineno and error_msg:
                msg += " (line {0}: {1}).".format(lineno, error_msg)
            elif lineno:
                msg += " (line {}).".format(lineno)
            elif error_msg:
                msg += " ({}).".format(error_msg)
            else:
                msg += "."
        super(ParamFileError, self).__init__(msg)
        self.filename = filename
        self.lineno = lineno
        self.error_msg = error_msg


class SimToolsWarning(Warning):
    """Base SimTools warning."""
    pass
