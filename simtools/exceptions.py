# -*- coding: utf-8 -*-
"""Exceptions and warnings raised by SimTools.

Exceptions include:

- FileError - raised during processing a file.
"""


class SimToolsError(Exception):
    """Base SimTools exception."""
    pass


class FileError(SimToolsError):
    """Error during processing a file."""

    def __init__(self, msg="", filename=None, lineno=None, error_msg=None,
                 line=None):
        if not msg and any((filename, lineno, error_msg, line)):
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
            if line:
                msg += "\n{}".format(line)
        super(FileError, self).__init__(msg)
        self.filename = filename
        self.lineno = lineno
        self.error_msg = error_msg
        self.line = line


class SimToolsWarning(Warning):
    """Base SimTools warning."""
    pass
