""" Put a description here """
from __future__ import print_function
from __future__ import absolute_import

__code_desc__ = "Put a description here"
__code_version__ = 'v2.1.1'
__code_debug__ = False

## Standard Libraries
import re
import logging
import argparse
from pprint import pprint,pformat

## Third Party Modules
import hvac

## Modules
try:
    from classes.Base import configureTLSValidation
    from classes.BuildingBlocks import BaseObject
    from classes.Exceptions import ValidationFailedError
except ImportError:
    from Base import configureTLSValidation
    from BuildingBlocks import BaseObject
    from Exceptions import ValidationFailedError

class HashiCorp(BaseObject):
    """
        Create a HashiCorp interface

        Before this can be used, the following must be set
        - key
        - cert
        - namespace
        - schema
        - base_url
        - port
    """

    #region: internal methods

    def __init__(self, loglevel='INFO', **kwargs):
        super().__init__()
        self._setProps()

        # create a map of attribute => (g/s)
        self.gs_fn = {
            'key':          (self.getHCVKeyFile,            self.setHCVKeyFile),
            'cert':         (self.getHCVCertificateFile,    self.setHCVCertificateFile),
            'schema':       (self.getHCVSchema,             self.setHCVSchema),
            'base_url':     (self.getHCVBaseUrl,            self.setHCVBaseUrl),
            'port':         (self.getHCVPort,               self.setHCVPort),
            'namespace':    (self.getHCVNamespace,          self.setHCVNamespace),
        }
        # Store kwargs locally in obj under init_params
        self.init_parameters = {}
        # Load em up
        for p in self.gs_fn.keys():
            try:
                val = self.init_parameters[p] = kwargs.pop(p)
                if val is not None:
                    gs = self.gs_fn[p]
                    set = gs[1]
                    set(val)
            except KeyError:
                self.init_parameters[p] = None

        ## Configure logging
        self.log = logging.getLogger(__name__)
        ## Configure TLS
        self._configureTLSValidation()
        self.kv_path = "kv-secrets/data/"
        self.re_kv_path = re.compile(rf"(?P<parameter>kv-secrets/data/(?P<argument>.*)")

    def _setProps(self):
        """ Ensure keys are set to avoid throwing attributeError, also perform class init """
        try:
            super()._setProps()
        except AttributeError:
            pass
        self.is_valid = False
        # validation_keys will be initialized to None, and checked when ready/validate is called
        self.validation_keys = ['key', 'cert', 'namespace', 'schema', 'base_url', 'port']
        # none_keys are additional keys to be set, but are not specifically needed to be set.
        # none_keys are typically built using a call to login()/auth()/etc, or are keys set via logging functions
        none_keys = [
            'auth_token', 'hvac_client', 'last_path', 'last_response'
        ]
        for k in none_keys + self.validation_keys:
            setattr(self, k, None)

    """
        Attempt to detect and configure TLS cert checking, allow caller to override in cases
        where the TLS for a given system/service is self-signed.
    """
    def _configureTLSValidation(self, disable_verification=False):
        verify, tls_bundle = configureTLSValidation(disable_verification=disable_verification)
        self.verify = verify
        self.tls_bundle = tls_bundle
        return

    #endregion: internal methods

    #region: private methods

    def _authenticated(self):
        if not self.validate():
            return False
        else:
            if self.auth_token is None:
                return False
            else:
                return True

    def _kv_read(self, path=None):
        arg = self.kv_path + path
        return self.readSecret(arg)

    #endregion: private methods

    #region: public methods

    def isLoggedIn(self):
        return self._authenticated()

    def loggedIn(self):
        return self._authenticated()

    def login(self, key=None, cert=None, schema=None, base_url=None, port=None, namespace=None):
        arguments = locals()
        del arguments['self']

        # if we have an auth_token, simply return the client back to the caller
        if self.auth_token is not None:
            return self.hvac_client

        # otherwise, check if we have what we need to instantiate a client and authenticate
        for k,v in arguments.items():
            g,s = self.gs_fn[k]
            if v is not None:
                s(v)

        b = self.validate()
        if not b:
            raise ValidationFailedError("Failed self.validate()")

        try:
            URI = '%s://%s:%d' % (self.schema, self.base_url, self.port)
            client = self.hvac_client = hvac.Client(
                url = URI,
                namespace = self.namespace,
                verify=self.tls_bundle
            )
            response = client.auth.cert.login(cert_pem=self.cert, key_pem=self.key)
            self.auth_token = response['auth']['client_token']
            return self.hvac_client
        except Exception as e:
            msg = "Caught Exception %s in login()" % (e)
            self.log.error(msg)
            raise e

    """ Stub Methods """
    def getHVACNamespace(self):
        return self.getHCVNamespace()

    def setHVACNamespace(self, namespace=None):
        return self.setHCVNamespace(namespace=namespace)

    #endregion: public methods

    #region: public interfaces

    def getHCVBaseUrl(self):
        return self.base_url

    def getHCVCertificateFile(self):
        return self.cert

    def getHCVKeyFile(self):
        return self.key

    def getHCVNamespace(self):
        return self.namespace

    def getHCVPort(self):
        return self.port

    def getHCVSchema(self):
        return self.schema

    def setHCVBaseUrl(self, base_url=None):
        self.base_url = base_url

    def setHCVCertificateFile(self, cert=None):
        self.cert = cert

    def setHCVKeyFile(self, key=None):
        self.key = key

    def setHCVNamespace(self, namespace=None):
        self.namespace = namespace

    def setHCVPort(self, port=8200):
        self.port = port

    def setHCVSchema(self, schema='https'):
        """ Only https is supported at this time """
        assert schema == "https"
        self.schema = schema

    def readSecretRaw(self, path=None):
        if self._authenticated():
            client = self.hvac_client

            try:
                self.last_path = path
                response = client.read(path)
                self.last_response = response
                return response
            except Exception as e:
                msg = "Caught Exception %s in readSecretRaw()" % (e)
                self.log.error(msg)
                raise e

        else:
            try:
                self.log.warning("ReadSecretRaw() called without a logged in session")
                self.log.warning("Attempting to login()")
                self.login()
                return self.readSecretRaw(path=path)
            except Exception as e:
                msg = "Unable to readSecretRaw() without a hvac_client, and attempts to login() failed for some reason"
                self.log.error(msg)
                raise Exception(msg)

    def readSecret(self, path=None):
        try:
            response = self.readSecretRaw(path=path)
            return response['data']['data']
        except TypeError as e:
            msg = "Caught Exception %s in readSecret(); the path to the secret may not be valid: (%s)" % (e, path)
            self.log.error(msg)
            raise e

    def KVReadSecret(self, path=None):
        match = self.re_kv_path.search(path)
        if match is not None:
            att = str(match.group('parameter')).strip()
            arg = str(match.group('argument')).strip()
            msg = "[RE] Found a match for %s: %s" % (att, arg)
            self.log.debug(msg)
            path = arg
        return self._kv_read(self, path)

    def validate(self):
        if self.AnyElementIsNone(self.validation_keys):
            self.is_valid = False
            return False
        else:
            self.is_valid = True
            return True

    #endregion: public interfaces


def demo(args):
    pass

def collect_args():
    parser = argparse.ArgumentParser(description=__code_desc__)
    parser.add_argument('-V', '--version', action='version', version=__code_version__)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--key', default="local.key",
        help="The private key to use to authenticate with: (default: %(default)s)" )
    parser.add_argument('--cert', default="local.pem",
        help="The public certificate to use to authenticate with: (default: %(default)s)" )
    parser.add_argument('--namespace', required=True, help="The HCV namespace to use")
    parser.add_argument('--secret', required=True, help="The path to a secret to read out of the vault")
    parser.add_argument('--env', default="TST", choices=['PRD','PRD1','PRD2','P1','P2','QUA','TST'],
            help="The environment to use: (default: %(default)s)" )

    args = parser.parse_args()
    return parser, args

def main():
    parser, args = collect_args()
    demo(args)

if __name__=="__main__":
    main()
