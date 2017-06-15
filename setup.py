#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

try:
    from setuptools import setup
except ImportError:
    raise ImportError(
        "Package 'setuptools' is required to proceed, but is not installed; "
        "please install it and try again")

testing = "test" in sys.argv or "pytest" in sys.argv

setup(
    name="simtools",
    version='0.1.0.dev1',
    author="Przemyslaw (Mack) Nowak",
    author_email="pnowak.mack@gmail.com",
    description="Python tools for simulation management",
    url="https://github.com/macknowak/simtools",
    license="GNU General Public License v3 or later (GPLv3+)",
    packages=['simtools'],
    setup_requires=['pytest-runner'] if testing else [],
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later '
        '(GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering'
        ]
    )
