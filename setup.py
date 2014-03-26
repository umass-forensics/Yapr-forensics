#!/usr/bin/env python

__author__ = 'rjwalls'
__author_email__ = 'rjwalls@cs.umass.edu'


from setuptools import setup, find_packages
import sys

requires = []

if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    requires += ['argparse']

setup(
    name = 'ypr',
    version = '0.1',
    packages = find_packages(),
    author = __author__,
    author_email = __author_email__,
    description = 'command line tool for parsing yaffs images',
    install_requires = requires,
    entry_points = {
        'console_scripts': [
            'yapr = ypr.yapr:main'
        ],
    }
)