#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Get Certificates from a request and dump them.
"""

import argparse
import sys

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

"""
Inspired by the answers from this Stackoverflow question:
https://stackoverflow.com/questions/16903528/how-to-get-response-ssl-certificate-from-requests-in-python

What follows is a series of patching the low level libraries in requests.
"""

"""
https://stackoverflow.com/a/47931103/622276
"""

sock_requests = requests.packages.urllib3.contrib.pyopenssl.WrappedSocket


def new_getpeercertchain(self, *args, **kwargs):
    x509 = self.connection.get_peer_cert_chain()
    return x509


sock_requests.getpeercertchain = new_getpeercertchain

"""
https://stackoverflow.com/a/16904808/622276
"""

HTTPResponse = requests.packages.urllib3.response.HTTPResponse
orig_HTTPResponse__init__ = HTTPResponse.__init__


def new_HTTPResponse__init__(self, *args, **kwargs):
    orig_HTTPResponse__init__(self, *args, **kwargs)
    try:
        self.peercertchain = self._connection.sock.getpeercertchain()
    except AttributeError:
        pass


HTTPResponse.__init__ = new_HTTPResponse__init__

HTTPAdapter = requests.adapters.HTTPAdapter
orig_HTTPAdapter_build_response = HTTPAdapter.build_response


def new_HTTPAdapter_build_response(self, request, resp):
    response = orig_HTTPAdapter_build_response(self, request, resp)
    try:
        response.peercertchain = resp.peercertchain
    except AttributeError:
        pass
    return response


HTTPAdapter.build_response = new_HTTPAdapter_build_response

"""
Attempt to wrap in a somewhat usable CLI
"""


def cli(args):
    parser = argparse.ArgumentParser(description="Request any URL and dump the certificate chain")
    parser.add_argument("url", metavar="URL", type=str, nargs=1, help="Valid https URL to be handled by requests")

    verify_parser = parser.add_mutually_exclusive_group(required=False)
    verify_parser.add_argument("--verify", dest="verify", action="store_true", help="Explicitly set SSL verification")
    verify_parser.add_argument(
        "--no-verify", dest="verify", action="store_false", help="Explicitly disable SSL verification"
    )
    parser.set_defaults(verify=True)

    return vars(parser.parse_args(args))


def dump_pem(cert, outfile="ca-chain.crt"):
    """Use the CN to dump certificate to PEM format"""
    PyOpenSSL = requests.packages.urllib3.contrib.pyopenssl
    pem_data = PyOpenSSL.OpenSSL.crypto.dump_certificate(PyOpenSSL.OpenSSL.crypto.FILETYPE_PEM, cert)
    issuer = cert.get_issuer().get_components()

    print(pem_data.decode("utf-8"))

    with open(outfile, "a") as output:
        for part in issuer:
            output.write(part[0].decode("utf-8"))
            output.write("=")
            output.write(part[1].decode("utf-8"))
            output.write(",\t")
        output.write("\n")
        output.write(pem_data.decode("utf-8"))


if __name__ == "__main__":
    cli_args = cli(sys.argv[1:])

    url = cli_args["url"][0]
    req = requests.get(url, verify=cli_args["verify"])
    for cert in req.peercertchain:
        dump_pem(cert)
