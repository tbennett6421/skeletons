from __future__ import (print_function,absolute_import)

__code_version__ = 'v0.0.0'

## Standard Libraries
import base64
import hashlib
from io import StringIO,BytesIO

## Third-Party
import numpy as np
import pandas as pd

## Modules
try:
    from .BuildingBlocks import BaseObject
except ImportError:
    from BuildingBlocks import BaseObject

class Serializer(BaseObject):

    def __init__(self):
        """ No special init needed for this class """
        super().__init__()
        self.is_valid = True

    def validate(self):
        """ No special validation needed for this class """
        self.is_valid = True
        return True


def demo():
    print("=== Demo ===")

def main():
    demo()

if __name__=="__main__":
    main()
