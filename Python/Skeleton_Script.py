#!/usr/bin/env python3

""" Put a description here """

from __future__ import print_function
from __future__ import absolute_import

__code_desc__ = "Put a description here"
__code_version__ = 'v0.0.1'
__code_debug__ = False

## Standard Libraries
import os
import sys
import argparse
from pprint import pformat, pprint

## Third Party libraries
## Modules

def main():
    parser = argparse.ArgumentParser(description=__code_desc__)
    parser.add_argument('-V', '--version', action='version', version=__code_version__)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.parse_args()
    pass

if __name__=="__main__":
    main()
