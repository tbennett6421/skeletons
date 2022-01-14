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
        """ Attempt to b64 encode a bytes-like object, coercing if needed """
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
                f"Data is of type: {type(data)}, unsure how to proceed",
            )
            raise TypeError(msg)

    def decode(self, data):
        """ Attempt to b64 decode a bytes-like object or string """
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

    def sha1sum(self, data):
        """ Attempt to hash a bytes-like object, coercing if needed """
        try:
            if isinstance(data, bytes):
                pass
            elif isinstance(data, str):
                data = data.encode()
            else:
                data = str(data).encode()
            return hashlib.sha1(data).hexdigest()
        except Exception as e:
            fx = inspect.currentframe().f_code.co_name
            msg = (
                f"In function: {fx}",
                f"Data is of type: {type(data)}, unsure how to proceed",
            )
            raise TypeError(msg)

def run_test(var, fx):
    """ call fx(var) and record details """
    print(f"[+] Testing method::{fx.__name__} against t({type(var)}) = {var}")
    ret = fx(var)
    print(f"[*] Result: {ret}")
    return ret

def unit_tests():
    s = Serializer()
    test_inputs = ['Hello', b'hello', 42, 3.14]
    vals = []
    try:
        for i in test_inputs:
            # b64encode various types and store output for later testing
            vals.append(run_test(i, getattr(s, 'encode')))

        # attempt to decode all values from prior
        for v in vals:
            run_test(v, getattr(s, 'decode'))

        # sha1sum various types and store output for later testing
        for i in test_inputs:
            run_test(i, getattr(s, 'sha1sum'))
        print("[*] End Tests")

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
