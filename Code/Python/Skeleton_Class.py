#!/usr/bin/env python3

""" Put a description here """

from __future__ import print_function
from __future__ import absolute_import

__code_desc__ = "Put a description here"
__code_version__ = 'v1.2.1'
__code_debug__ = True

## Standard Libraries
import os
import sys
from pprint import pformat, pprint

## Third Party libraries

## Modules
try:
    from classes.BuildingBlocks import State, BaseObject
except ImportError:
    try:
        from .BuildingBlocks import State, BaseObject
    except ImportError:
        from BuildingBlocks import State, BaseObject

class Skeleton_Class(BaseObject):

    def __init__(self):
        #region: debugging handler
        if __code_debug__:
            try:
                import debugpy
                debugpy.listen(5678)
                print("Waiting for debugger attach")
                debugpy.wait_for_client()
                debugpy.breakpoint()
                print('break on this line')
            except ImportError:
                import ptvsd
                print("Waiting for debugger attach")
                ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
                ptvsd.wait_for_attach()
                breakpoint()
                print('break on this line')
        #endregion: debugging handler

        ## Call parent init
        super().__init__()

    def validate(self):
        ## Assume not valid
        self.is_valid = False

        ## Do checking logic, if all checks succeed you should set is_valid to True
        ## -----------------------

        return self.is_valid


def demo():
    print("=== Demo ===")
    print("Example usage/code goes here")

def main():
    demo()

if __name__=="__main__":
    main()
