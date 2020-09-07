#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

try:
    from setuptools import setup
except ImportError:
    raise ImportError(
        "Package 'setuptools' is required to proceed, but is not installed; "
        "please install it and try again")

setup_path = os.path.abspath(os.path.dirname(__file__))


def read_description(filename):
    with open(os.path.join(setup_path, filename), 'r') as description_file:
        return description_file.read()


setup(
    name="simtools",
    version='0.1.0.dev1',
    author="Przemyslaw (Mack) Nowak",
    author_email="pnowak.mack@gmail.com",
    description="Python tools for simulation management",
    long_description=read_description("README.md"),
    long_description_content_type='text/markdown',
    url="https://github.com/macknowak/simtools",
    license="GNU General Public License v3 or later (GPLv3+)",
    packages=['simtools', 'simtools.bin'],
    entry_points={
        'console_scripts': [
            'exppar = simtools.bin.exppar:main',
            'genseed = simtools.bin.genseed:main',
            'runsim = simtools.bin.runsim:main'
            ]
        },
    extras_require={'tests': "pytest"},
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 or later '
        '(GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering'
        ]
    )
