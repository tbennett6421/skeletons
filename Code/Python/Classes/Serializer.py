from __future__ import (print_function,absolute_import)

__code_version__ = 'v0.0.0'

## Standard Libraries
import inspect
import base64
import hashlib
from io import StringIO,BytesIO

## Third-Party
try:
    import numpy as np
    import pandas as pd
except ModuleNotFoundError:
    pass

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

    def encode(self, data):
        """ attempt to b64 encode a bytes-like object, coercing if needed """
        try:
            if isinstance(data, bytes):
                pass
            elif isinstance(data, str):
                data = data.encode()
            else:
                data = str(data).encode()
            return base64.b64encode(data)
        except Exception as e:
            fx = inspect.currentframe().f_code.co_name
            msg = (
                f"In function: {fx}",
                f"Data is of type: {type(data)}, unsure how to base64encode",
            )
            raise TypeError(msg)

    def decode(self, data):
        """ attempt to b64 decode a bytes-like object or string"""
        try:
            if isinstance(data, bytes) or isinstance(data, str):
                return base64.b64decode(data)
            else:
                fx = inspect.currentframe().f_code.co_name
                msg = (
                    f"In function: {fx}",
                    f"Data is of type: {type(data)}, unsure how to base64decode",
                )
                raise TypeError(msg)
        except Exception as e:
            print(e)

def run_test(var, fx):
    """ call fx(var) and record details """
    print(f"[+] Testing method::{fx.__name__} against t({type(var)}) = {var}")
    ret = fx(var)
    print(f"[*] Result: {ret}")
    return ret

def unit_tests():
    s = Serializer()
    vals = []
    try:
        vals.append(run_test("Hello", getattr(s, 'encode')))
        vals.append(run_test(b"Hello", getattr(s, 'encode')))
        vals.append(run_test(42, getattr(s, 'encode')))
        vals.append(run_test(3.14, getattr(s, 'encode')))

        for v in vals:
            run_test(v, getattr(s, 'decode'))
        print()

    except Exception as e:
        print(e)
        raise e

def demo():
    print("Running unit_tests")
    unit_tests()
    print("=== Demo ===")

def main():
    demo()

if __name__=="__main__":
    main()
