""" Put a description here """

from __future__ import print_function
from __future__ import absolute_import

__code_desc__ = "Encapsulate elasticsearch-dsl library"
__code_version__ = 'v4.1.1'
__code_debug__ = False

## Standard Libraries
from pprint import pprint
from ssl import create_default_context

## Third Party libraries
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

## Modules
try:
    from classes.BuildingBlocks import BaseObject
    from classes.CyberArk import CyberArk
    from classes.Exceptions import ValidationFailedError
except ImportError:
    from BuildingBlocks import BaseObject
    from CyberArk import CyberArk
    from Exceptions import ValidationFailedError

class Elastic(BaseObject):
    """
        Create an Elastic interface

        Before this can be used, the following must be set
        - hosts
        - port
        - schema
        - ssl_context
        - username
        - password
    """

    #region: internal methods

    def __init__(self, hosts=None, port=None, schema=None, ssl_context=None, username=None, password=None, loglevel="INFO"):
        if __code_debug__:
            loglevel = "DEBUG"
        super().__init__(loglevel=loglevel)
        self._set_props()
        self.setHosts(hosts)
        self.setPort(port)
        self.setSchema(schema)
        self.setSSLContext(ssl_context)
        self.setUsername(username)
        self.setPassword(password)

    def _set_props(self):
        """ Ensure keys are set to avoid throwing attributeError, also perform class init """
        self.is_valid = False
        self.is_connected = False
        self.es_default_port = 9200
        self.validation_keys = ['hosts', 'port', 'schema', 'ssl_context', 'username', 'password']
        none_keys = [
            'es_client', 'last_search', 'last_response', 'last_response_meta',
        ]
        for k in none_keys + self.validation_keys:
            setattr(self, k, None)

    def _build_ssl_context(self, ssl_context=None, cafile='/etc/pki/tls/certs/ca-bundle.crt'):
        if ssl_context is None:
            try:
                ssl_context = create_default_context(cafile=cafile)
                return ssl_context
            except FileNotFoundError:
                ssl_context = create_default_context()
                return ssl_context
        else:
            return ssl_context

    def _AnyElementIsNone(self, lst):
        """
            Check a provided list if any element is None; Used for validation checks
            Return:
                True is anything in the list is None
                False if all checks proceeded successfully
        """
        try:
            for k in lst:
                attr = getattr(self, k)
                if attr is None:
                    return True
            return False
        except KeyError as e:
            print(e)
            return True
        except Exception as e:
            raise e

    def debugSelf(self):
        hardcoded_class = "Elastic"
        hardcoded_baseclass = "BaseObject"
        print("//%s" % ("-"*80))
        print("// %s" % str(self.__class__))
        print("// %s" % str(hardcoded_class))
        print("// %s: %s" % ("__code_desc__", str(__code_desc__)))
        print("// %s: %s" % ("__code_version__", str(__code_version__)))
        print("// %s: %s" % ("__code_debug__", str(__code_debug__)))
        print("//%s" % ("-"*80))
        print("%s.%s: %s" % ( hardcoded_baseclass, "keys()", str(self.keys()) ))
        print("%s.%s: %s" % ( hardcoded_baseclass, "meta()", str(self.meta()) ))
        print("%s.%s: %s" % ( hardcoded_baseclass, "is_valid", str(self.is_valid) ))
        print("%s.%s: %s" % ( hardcoded_baseclass, "is_connected", str(self.is_connected) ))
        print("%s.%s: %s" % ( hardcoded_baseclass, "ready()", str(self.ready()) ))
        print("%s.%s: %s" % ( hardcoded_class, "hosts", str(self.hosts) ))
        print("%s.%s: %s" % ( hardcoded_class, "port", str(self.port) ))
        print("%s.%s: %s" % ( hardcoded_class, "schema", str(self.schema) ))
        print("%s.%s: %s" % ( hardcoded_class, "ssl_context", str(self.ssl_context) ))
        print("%s.%s: %s" % ( hardcoded_class, "username", str(self.username) ))
        print("%s.%s: %s" % ( hardcoded_class, "password", "REDACTED" ))
        print("%s.%s: %s" % ( hardcoded_class, "es_client", str(self.es_client) ))
        print("%s.%s: %s" % ( hardcoded_class, "es_default_port", str(self.es_default_port) ))
        print("%s.%s: %s" % ( hardcoded_class, "last_search", str(self.last_search) ))
        print("%s.%s: %s" % ( hardcoded_class, "last_response", str(self.last_response) ))
        print("%s.%s: %s" % ( hardcoded_class, "last_response_meta", str(self.last_response_meta) ))
        print("%s.%s: %s" % ( hardcoded_class, "validate()", str(self.validate()) ))
        try:
            print("%s.%s: %s" % ( hardcoded_class, "numberOfHits()", str(self.numberOfHits()) ))
            print("%s.%s: %s" % ( hardcoded_class, "queryHitCount()", str(self.queryHitCount()) ))
            print("%s.%s: %s" % ( hardcoded_class, "querySuccess()", str(self.querySuccess()) ))
            print("%s.%s: %s" % ( hardcoded_class, "success()", str(self.success()) ))
        except:
            pass
        print("//%s" % ("-"*80))

    #endregion: internal methods

    #region: private methods

    # Only support http_auth and tls clusters at this time
    def buildClient(self, hosts=None, port=None, schema=None, ssl_context=None, username=None, password=None):
        # if caller supplies any params, persist them to the object for validation() checks
        if hosts is not None:
            self.setHosts(hosts)
        else:
            hosts = self.getHosts(throw=True)

        if port is not None:
            self.setPort(port)
        else:
            port = self.getPort(throw=True)

        if schema is not None:
            self.setSchema(schema)
        else:
            schema = self.getSchema(throw=True)

        if ssl_context is not None:
            self.setSSLContext(ssl_context)
        else:
            ssl_context = self.getSSLContext(throw=True)

        if username is not None:
            self.setUsername(username)
        else:
            username = self.getUsername(throw=True)

        if password is not None:
            self.setPassword(password)
        else:
            password = self.getPassword(throw=True)

        # at this point, all params should be set, otherwise exceptions should be thrown
        if self._AnyElementIsNone(['hosts', 'port', 'schema', 'ssl_context', 'username', 'password']):
            raise AssertionError()

        self.es_client = Elasticsearch(
            hosts,
            http_auth=(username, password),
            scheme=schema,
            port=port,
            ssl_context=ssl_context,
        )
        self.is_valid = True
        self.is_connected = True
        return self.es_client

    def buildSimpleSearch(self, index=None, field=None, value=None):
        """
            Search an index for an field and value
                @param index may use wildcards
        """
        assert index is not None
        assert field is not None
        assert value is not None
        s = Search(using=self.es_client, index=index) \
            .query('match', **{field: value})
        self.last_search = s
        return s

    def buildComplexSearch(self, index=None, fieldsDict=None):
        """
            Search an index for multiple field,value pairs
                @param index may use wildcards
        """
        assert index is not None
        assert fieldsDict is not None
        s = Search(using=self.es_client, index=index)
        for field,value in fieldsDict.items():
            s = s.query('match', **{field: value})
        self.last_search = s
        return s

    def executeSearch(self, search=None):
        assert search is not None
        assert self.connected() is True
        # Execute search and return response, generator
        response = self.last_response = search.execute()
        search.params(preserve_order=True)
        generator = self.last_response = search.scan()
        return response, generator

    #endregion: private methods

    #region: public methods

    def responseDetails(self, response=None):
        assert response is not None
        meta = self.last_response_meta = {
            "success": response.success(),
            "ms": response.took,
            "hitCount": response.hits.total,
        }
        return meta

    def responseToRaw(self, response=None):
        assert response is not None
        return response.to_dict()

    def responseToHits(self, response=None):
        assert response is not None
        try:
            resp = self.responseToRaw(response)
            return resp['hits']['hits']
        except Exception as e:
            pprint(e)

    def querySuccess(self, response=None):
        """ Return the status of the response (optionally) or the last known response """
        if response is None:
            try:
                return bool(self.last_response_meta['success'])
            except Exception as e:
                print("Caught Exception %s in querySuccess()" % (e) )
                return False
        else:
            try:
                meta = self.responseDetails(response=response)
                return bool(meta['success'])
            except Exception as e:
                print("Caught Exception %s in querySuccess()" % (e) )
                return False

    def queryHitCount(self, response=None):
        """ Return the last hit count of the response (optionally) or the last known response """
        if response is None:
            try:
                return self.last_response_meta['hitCount']
            except Exception as e:
                print("Caught Exception %s in querySuccess()" % (e) )
                return False
        else:
            try:
                meta = self.responseDetails(response=response)
                return meta['hitCount']
            except Exception as e:
                print("Caught Exception %s in querySuccess()" % (e) )
                return False

    def success(self, response=None):
        """ convenience stub """
        return self.querySuccess(response=response)

    def numberOfHits(self, response=None):
        """ convenience stub """
        return self.queryHitCount(response=response)

    #endregion: public methods

    #region: public interfaces

    def validate(self):
        if self.es_client is not None:
            self.is_valid = True
            self.is_connected = True
            return True
        else:
            if self._AnyElementIsNone(self.validation_keys):
                self.is_valid = False
                self.is_connected = False
                return False
            else:
                self.is_valid = True
                self.is_connected = False
                return True

    def connected(self):
        return self.is_connected

    def connect(self):
        """ Connect to the ES cluster and build a suitable client """
        if self.connected():
            return self.es_client
        elif self.validate():
            self.es_client = self.buildClient()
            return self.es_client
        else:
            raise ValidationFailedError("Failed self.validate()")

    def search(self, index=None, field=None, value=None, fieldsDict=None):
        """
            Construct a Search() and execute it
                returns: response, generator, and response_metadata
        """
        assert index is not None
        assert (field is not None and value is not None) or (fieldsDict is not None)
        assert self.connected() is True
        if fieldsDict is None:
            s = self.buildSimpleSearch(index=index, field=field, value=value)
            r, g = self.executeSearch(search=s)
        else:
            s = self.buildComplexSearch(index=index, fieldsDict=fieldsDict)
            r, g = self.executeSearch(search=s)
        return r, g, self.responseDetails(r)

    def getHosts(self, throw=False):
        if throw:
            if self.hosts is None:
                raise ValueError('%s is None and exception throwing was requested' % ('self.hosts') )
            else:
                return self.hosts
        return self.hosts

    def getPort(self, throw=False):
        if throw:
            if self.port is None:
                raise ValueError('%s is None and exception throwing was requested' % ('self.port') )
            else:
                return self.port
        return self.port

    def getSchema(self, throw=False):
        if throw:
            if self.schema is None:
                raise ValueError('%s is None and exception throwing was requested' % ('self.schema') )
            else:
                return self.schema
        return self.schema

    def getSSLContext(self, throw=False):
        if throw:
            if self.ssl_context is None:
                raise ValueError('%s is None and exception throwing was requested' % ('self.ssl_context') )
            else:
                return self.ssl_context
        return self.ssl_context

    def getUsername(self, throw=False):
        if throw:
            if self.username is None:
                raise ValueError('%s is None and exception throwing was requested' % ('self.username') )
            else:
                return self.username
        return self.username

    def getPassword(self, throw=False):
        if throw:
            if self.password is None:
                raise ValueError('%s is None and exception throwing was requested' % ('self.password') )
            else:
                return self.password
        return self.password

    def setHosts(self, param):
        self.hosts = param

    def setPort(self, param):
        self.port = param

    def setSchema(self, param):
        self.schema = param

    def setSSLContext(self, param):
        self.ssl_context = param

    def setUsername(self, param):
        self.username = param

    def setPassword(self, param):
        self.password = param

    #endregion: public interfaces

def demo():
    pass

def main():
    demo()

if __name__=="__main__":
    main()
