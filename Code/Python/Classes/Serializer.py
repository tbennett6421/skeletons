from __future__ import (print_function,absolute_import)

__code_version__ = 'v0.0.0'

## Standard Libraries
import sys
import inspect
import pickle
import base64
import hashlib
from io import BytesIO#,StringIO
from pprint import pprint

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

class Serialized_Container(BaseObject):

    def __init__(self):
        """ No special init needed for this class """
        super().__init__()
        self.acceptable_metadata = {
            'size_of_data': "The size of the data (in bytes) prior to being serialized",
            'size_of_pickle': "The size of the data (in bytes) of the pickled object",
            'encoded_pickle': "The pickle's representation as encoded via base64()",
            'pickle_hash': "The hash calculated against the pickle or 'payload'",
            'pickle_hash_method': "Identifies the message digest used to create pickle_hash",
            'encoding_hash': "The hash calculated against the base64 encoded payload or 'carrier'",
            'encoding_hash_method': "Identifies the message digest used to create encoding_hash",
        }
        self.acceptable_metadata_keys = self.acceptable_metadata.keys()
        self.__init_vars__()

    def __init_vars__(self):
        for k in self.acceptable_metadata_keys:
            setattr(self, k, None)
        self.is_valid = True

    def pretty_print(self, print_to_console=True):
        fx = inspect.currentframe().f_code.co_name
        console_buffer = []
        for k in self.acceptable_metadata_keys:
            try:
                v = getattr(self, k)
                fstr = f"key({k}) => val({v})"
                console_buffer.append(fstr)
                if print_to_console:
                    print(fstr)
            except AttributeError:
                msg = (
                    f"In function: {fx}",
                    f"Failed to access attribute: {k}; ignoring",
                )
                print(msg)
                continue
        return console_buffer

    def load_dump(self, dump):
        fx = inspect.currentframe().f_code.co_name
        for k in self.acceptable_metadata_keys:
            try:
                setattr(self, k, dump[k])
            except AttributeError:
                msg = (
                    f"In function: {fx}",
                    f"Failed to load attribute: {k}; ignoring",
                )
                print(msg)
                continue
        print(self)

    def to_pickle(self):
        """
            Given the classes metadata; attempt to load the pickle safely by running hash checks
            returns the decoded pickle on success
        """
        try:
            if isinstance(self.encoded_pickle, bytes):
                pass
            else:
                # Convert to bytes object if needed
                self.encoded_pickle = str(self.encoded_pickle).encode()

            s = Serializer()
            carrier = self.encoded_pickle

            # # sha1sum and compare to stored hash in metadata
            prior = s.sha1sum(carrier)
            assert(prior == self.encoding_hash)

            # decode(sha1(payload)) and compare to stored hash in metadata
            payload = s.decode(carrier)
            post = s.sha1sum(payload)
            assert(post == self.pickle_hash)

            # if successful,
            pickle_buffer = BytesIO(payload)
            return True, pickle_buffer

        except AssertionError:
            return False, None

    def validate(self):
        """ No special validation needed for this class """
        self.is_valid = True
        return True

class Serializer(BaseObject):

    def __init__(self):
        """ No special init needed for this class """
        super().__init__()
        self.is_valid = True

    def validate(self):
        """ No special validation needed for this class """
        self.is_valid = True
        return True

    def _serialize_df(self, df):
        """ This method takes a pandas dataframe and serializes it """
        pickle_buffer = BytesIO()
        df.to_pickle(pickle_buffer)
        return pickle_buffer.getvalue()

    def _serialize_np(self, nd):
        """ This method takes a numpy array and serializes it """
        pickle_buffer = BytesIO()
        np.save(pickle_buffer, nd)
        return pickle_buffer.getvalue()

    def size_of(self, data):
        return sys.getsizeof(data)

    def encode(self, data):
        """ Attempt to b64 encode a bytes-like object, coercing if needed """
        fx = inspect.currentframe().f_code.co_name
        try:
            if isinstance(data, bytes):
                pass
            elif isinstance(data, str):
                data = data.encode()
            elif isinstance(data, np.ndarray):
                msg = (
                    f"In function: {fx}",
                    f"Data is of type: {type(data)}, you should serialize this first",
                )
                raise TypeError(msg)
            else:
                data = str(data).encode()
            return base64.b64encode(data)
        except TypeError as e:
            raise e
        except Exception as e:
            msg = (
                f"In function: {fx}",
                f"Data is of type: {type(data)}, unsure how to proceed",
            )
            raise TypeError(msg)

    def decode(self, data):
        """ Attempt to b64 decode a bytes-like object or string """
        fx = inspect.currentframe().f_code.co_name
        try:
            if isinstance(data, bytes) or isinstance(data, str):
                return base64.b64decode(data)
            else:
                msg = (
                    f"In function: {fx}",
                    f"Data is of type: {type(data)}, unsure how to base64decode",
                )
                raise TypeError(msg)
        except Exception as e:
            print(e)

    def sha1sum(self, data):
        """ Attempt to hash a bytes-like object, coercing if needed """
        fx = inspect.currentframe().f_code.co_name
        try:
            if isinstance(data, bytes):
                pass
            elif isinstance(data, str):
                data = data.encode()
            elif isinstance(data, np.ndarray):
                msg = (
                    f"In function: {fx}",
                    f"Data is of type: {type(data)}, you should serialize this first",
                )
                raise TypeError(msg)
            else:
                data = str(data).encode()
            return hashlib.sha1(data).hexdigest()
        except Exception as e:
            msg = (
                f"In function: {fx}",
                f"Data is of type: {type(data)}, unsure how to proceed",
            )
            raise TypeError(msg)

    def serialize(self, data):
        try:
            if isinstance(data, pd.DataFrame):
                return self._serialize_df(data)
            elif isinstance(data, np.ndarray):
                return self._serialize_np(data)
            else:
                pickle_buffer = BytesIO()
                pickle.dump(data, pickle_buffer)
                return pickle_buffer.getvalue()
        except Exception as e:
            print(e)
            raise e

    def dump(self, data):
        """
            This method attempts to
                collect bytesize info
                serialize input,
                hashs the pickle
                encodes the pickle
                and hashs the encoded repr
            and return pickle, and metadata
        """
        try:
            pdata = self.serialize(data)
            b64 = self.encode(pdata)
            meta = {
                'size_of_data': self.size_of(data),
                'size_of_pickle': self.size_of(pdata),
                'encoded_pickle': b64,
                'pickle_hash': self.sha1sum(pdata),
                'pickle_hash_method': 'SHA1',
                'encoding_hash': self.sha1sum(b64),
                'encoding_hash_method': 'SHA1',
            }
            return pdata, meta
        except Exception as e:
            print(e)
            raise e

def _task_runner(var, fx, verbose=True, print_result=True):
    """ call fx(var) and record details """
    try:
        if verbose:
            print(f"[+] Testing method::{fx.__name__} against t({type(var)})")
            print(var)

        ret = fx(var)
        if verbose and print_result:
            print(f"[>] Result: {ret}")
        return ret
    except Exception as e:
        print(e)
        raise e

def run_test(var, fx):
    return _task_runner(var, fx, verbose=True, print_result=True)

def run_dump_test(var, fx):
    return _task_runner(var, fx, verbose=True, print_result=False)

def unit_tests():
    s = Serializer()
    a1D = np.array([1, 2, 3, 4])
    a2D = np.array([[1, 2], [3, 4]])
    a3D = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
    df1D = pd.DataFrame(a1D, columns = ['Column_A'])

    test_inputs1 = ['Hello', b'hello', 42, 3.14]
    test_inputs2 = [a1D, a2D, a3D]
    test_inputs3 = [df1D]
    test_inputs = test_inputs1 + test_inputs2 + test_inputs3

    encoded_vals = []
    serialized_objs = []
    try:
        for i in test_inputs1:
            # b64encode various types and store output for later testing
            encoded_vals.append(run_test(i, getattr(s, 'encode')))

        # attempt to decode all values from prior
        for v in encoded_vals:
            run_test(v, getattr(s, 'decode'))

        # sha1sum various types
        for i in test_inputs1:
            run_test(i, getattr(s, 'sha1sum'))

        # serialize all object and store for later testing
        for i in test_inputs:
            serialized_objs.append(run_test(i, getattr(s, 'serialize')))

        # sha1sum serialized objects
        for i in serialized_objs:
            run_test(i, getattr(s, 'sha1sum'))

        # get bytesizes for various types
        for i in test_inputs:
            run_test(i, getattr(s, 'size_of'))
        print("[*] End basic tests")

        print("[*] Begin dumping tests")
        for i in test_inputs:
            run_dump_test(i, getattr(s, 'dump'))

    except Exception as e:
        print(e)
        raise e

def demo():
    print("=== Demo ===")

    s = Serializer()
    nd = np.array([1, 2, 3, 4])
    df = pd.DataFrame(nd, columns = ['Column_A'])

    nd_pickle, nd_meta = s.dump(nd)
    df_pickle, df_meta = s.dump(df)

    print(nd_meta)
    print(df_meta)
    print()

    pkg = Serialized_Container()
    pkg.load_dump(df_meta)
    pkg.pretty_print()
    b, p = pkg.to_pickle()
    if b:
        print("[*] Successfully unpickled df_meta")
        print(f"[*] pickle => {p}")

def main():
    demo()
    print("Running unit_tests")
    print()
    unit_tests()

if __name__=="__main__":
    main()
