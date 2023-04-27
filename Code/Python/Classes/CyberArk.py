#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

__code_version__ = 'v4.1.3'

## Standard Libraries
import time
from urllib.parse import quote

## Third-Party
from requests.exceptions import HTTPError,SSLError

## Modules
try:
    from classes.Base import askForCredentials,getArgsLikeObject,isIterableCollection
    from classes.WebClient import WebClient
except ImportError:
    from Base import askForCredentials,getArgsLikeObject,isIterableCollection
    from WebClient import WebClient

class CyberArkResponse(object):

    def __init__(self, properties):
        self.vault = {}
        self.epv_base_url = aca.epv_base_url
        self.ccp_base_url = aca.ccp_base_url
        self.ConstructVault(properties)

    def _vaultGet(self, key):
        """ Attempt to access key, handling errors. """
        try:
            return self.vault[str(key)]
        except KeyError:
            return None

    def _vaultInit(self, key, initargs):
        """ This is used for creating the vault from a response argument. """
        try:
            key = str(key)
            self.vault[key] = initargs[key]
            return True
        except KeyError:
            return False

    def _vaultAdd(self, key, value):
        """ This is used for arbitrarily adding kv args. """
        try:
            self.vault[str(key)] = value
            return True
        except Exception:
            return False

    def ConstructVault(self, initargs):
        for k,v in initargs.items():
            self._vaultInit(k, initargs)

    def getFolder(self):
        return self._vaultGet("Folder")

    def getName(self):
        return self._vaultGet("Name")

    def getDeviceType(self):
        return self._vaultGet("DeviceType")

    def getPassword(self):
        return self._vaultGet("Content")

    def getPolicyID(self):
        return self._vaultGet("PolicyID")

    def getSafe(self):
        return self._vaultGet("Safe")

    def getUsername(self):
        return self._vaultGet("UserName")

    def getCredentials(self):
        usernm = self.getUsername()
        passwd = self.getPassword()
        return usernm, passwd

    def getVault(self):
        return self.vault

    def setFolder(self, value):
        return self._vaultAdd("Folder", value)

    def setName(self, value):
        return self._vaultAdd("Name", value)

    def setDeviceType(self, value):
        return self._vaultAdd("DeviceType", value)

    def setPassword(self, value):
        return self._vaultAdd("Content", value)

    def setPolicyID(self, value):
        return self._vaultAdd("PolicyID", value)

    def setSafe(self, value):
        return self._vaultAdd("Safe", value)

    def setUsername(self, value):
        return self._vaultAdd("UserName", value)

class CCPResponse(CyberArkResponse):
    """ Accepts CCP RJSN as init """
    def __init__(self, properties):
        self.initargs = {}
        for k,v in properties.items():
            k = str(k).replace('-', '')
            self.initargs[k] = v
        super().__init__(self.initargs)

class EPVResponse(CyberArkResponse):
    """ Accepts EPV respJSON['accounts'][0] as init """
    def __init__(self, account, auth_token):
        self.accountid = account["AccountID"]
        self.initargs = {"AccountID": self.accountid}
        properties = account["Properties"]
        for prop in properties:
            k = str(prop["Key"]).replace('-', '')
            self.initargs[k] = prop["Value"]
        super().__init__(self.initargs)
        self.auth_token = auth_token
        passwd = self.EPVGetPassword(self.accountid)
        self.setPassword(passwd)

    def EPVGetPassword(self, aid):
        try:
            password_url = "%s/%s/%s" % (self.epv_base_url, aid, "Credentials")
            headers = {
                "Authorization": self.auth_token,
            }
            wc = WebClient()
            rcode, resp = wc.get(password_url, headers=headers)
            self.password = resp.text
            if self.password == '':
                self.password = None
            return self.password
        except:
            raise

class CyberArk(WebClient):
    """
        Create a CyberArk interface

        Before this can be used, the following must be set
        - ccp_base_url
        - epv_base_url
        - epv_logon_url
        - ca_appid
        - ca_safe
        - ca_object
    """

    #region: internal methods

    def __init__(self, ca_appid=None, ca_safe=None, ca_object=None, loglevel='INFO', disable_verification=False, ccp_base_url=None, epv_base_url=None, epv_logon_url=None):
        ## Call parent init
        super().__init__(disable_verification=disable_verification)
        self._setProps()
        self.setCAParams(ca_appid, ca_safe, ca_object)
        self.setCCPBaseUrl(ccp_base_url)
        self.setEPVBaseUrl(epv_base_url)
        self.setEPVLogonUrl(epv_logon_url)

    def _setProps(self):
        """ Ensure keys are set to avoid throwing attributeError, also perform class init """
        try:
            super()._setProps()
        except AttributeError:
            pass
        self.is_valid = False
        self.auth_token = None
        self.validation_keys = [
            'ccp_base_url', 'ca_appid', 'ca_safe', 'ca_object', 'epv_base_url', 'epv_logon_url',
        ]
        none_keys = list(self.validation_keys)
        none_keys = none_keys + ['auth_token', 'auth_username', 'auth_password', 'vault', 'vault_method']
        for k in none_keys:
            setattr(self, k, None)

    def _checkListIfAnyElementIsNone(self, lst):
        """
            Check a provided list if any element is None/Empty; Used for validation checks
            Return:
                True is anything in the list is None/Empty
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

    #endregion: internal methods

    #region: private methods

    def buildParams(self):
        return {
        'AppId': self.ca_appid,
        'Safe': self.ca_safe,
        'Object': self.ca_object
    }

    def setCAParams(self, ca_appid=None, ca_safe=None, ca_object=None):
        self.setCAAppid(ca_appid)
        self.setCASafe(ca_safe)
        self.setCAObject(ca_object)

    def _authenticated(self):
        if not self.validate():
            return False
        else:
            if self.auth_token is None:
                return False
            else:
                return True

    def authenticateUser(self, username, password):
        headers = {
            "Accept": "application/json",
            "ContentType": "application/json",
        }
        body = {
            "username": username,
            "password": password,
            "useRadiusAuthentication": True,
            "connectionnumber": "1",
        }
        print("Making POST request to logon: %s" % (self.epv_logon_url))
        print("Check MS Authenticator for MFA response")
        rcode, resp = self.post(self.epv_logon_url, headers=headers, json=body)
        respJson = resp.json()
        return respJson['CyberArkLogonResult']

    #endregion: private methods

    #region: public methods

    def isLoggedIn(self):
        return self._authenticated()

    def loggedIn(self):
        return self._authenticated()

    def validate(self):
        """ Ensure username/password/vars configured
            Signals class is ready to communicate with CyberArk
        """
        try:
            ## Check if any urls are missing
            if self._checkListIfAnyElementIsNone(self.validation_keys):
                self.is_valid = False
                return False
            else:
                self.is_valid = True
                return True
        except KeyError as e:
            print(e)
            self.is_valid = False
            return False
        except Exception as e:
            raise e

    def setAuthUsername(self, username=None):
        self.auth_username = username

    def setAuthPassword(self, password=None):
        self.auth_password = password

    def getAuthUsername(self):
        try:
            return self.auth_username
        except Exception:
            return None

    def getAuthPassword(self):
        try:
            return self.auth_password
        except Exception:
            return None

    #endregion: public methods

    #region: public interfaces

    def fetchCredentials(self, username=None, password=None):
        # Check if ready(), if not, attempt to validate(), re-check and recall self
        if not self.ready():
            self.validate()
            _ = self.ready(throw=True, message="Not ready(), after calling self.validate()")
            return self.fetchCredentials(username=username, password=password)
        else:
            successful = False
            if not successful:
                # Try CCP first
                try:
                    self.fetchCredentialsViaCCP()
                    successful = True
                except HTTPError:
                    self.log.warning("[!] Caught HTTPError when calling CCP")
                except SSLError:
                    self.log.warning("[!] Caught SSLError when calling CCP")

            if not successful:

                # Resolve credentials. At the end of the chain,
                # we should have a valid self.auth_username, self.auth_password
                if not self.auth_username or not self.auth_password:
                    if not username or not password:
                        # If no creds; Ask for creds
                        username, password = askForCredentials("Please provide credentials to connect to EPV")
                        self.setAuthUsername(username)
                        self.setAuthPassword(password)
                    else:
                        # If creds; set/persist to object
                        self.setAuthUsername(username)
                        self.setAuthPassword(password)

                # Try EPV, up to 5 times, with a delay
                for i in range(5):
                    try:
                        time.sleep(1)
                        self.fetchCredentialsViaEPV(username=self.auth_username, password=self.auth_password)
                        successful = True
                        break
                    except HTTPError:
                        self.log.warning("[!] Caught HTTPError when calling EPV")
                    except SSLError:
                        self.log.warning("[!] Caught SSLError when calling EPV")

    def fetchCredentialsViaCCP(self):
        """ fetchCredentialsViaCCP uses the CCP endpoint to authenticate against CyberArk using a trusted IP. """
        # Check if ready(), if not, attempt to validate(), re-check and recall self
        if not self.ready():
            self.validate()
            _ = self.ready(throw=True, message="Not ready(), after calling self.validate()")
            return self.fetchCredentialsViaCCP()
        else:
            try:
                params = self.buildParams()
                rcode, resp = self.get(url=self.ccp_base_url, params=params)
                rjsn = resp.json()
                ccpr = CCPResponse(properties=rjsn)
                self.vault_method = "CCP"
                self.vault = ccpr
                self.is_valid = True
            except Exception:
                raise

    def fetchCredentialsViaEPV(self, username=None, password=None):
        """
            fetchCredentialsViaEPV is used to authenticate to epv and pull creds
            for instance, when operating from a developer workstation.
        """
        # Check if ready(), if not, attempt to validate(), re-check and recall self
        if not self.ready():
            self.validate()
            _ = self.ready(throw=True, message="Not ready(), after calling self.validate()")
            return self.fetchCredentialsViaEPV(username=username, password=password)
        else:

            if not self.auth_username or not self.auth_password:
                if not username or not password:
                    # If no creds; Ask for creds
                    username, password = askForCredentials("Please provide credentials to connect to EPV")
                    self.setAuthUsername(username)
                    self.setAuthPassword(password)
                else:
                    # If creds; set/persist to object
                    self.setAuthUsername(username)
                    self.setAuthPassword(password)

            # Get a token if needed
            if not self.auth_token:
                self.auth_token = self.authenticateUser(username=self.auth_username, password=self.auth_password)

            try:
                account_url = self.epv_base_url
                self.params = self.buildParams()
                headers = {
                    "Accept": "application/json",
                    "Authorization": self.auth_token,
                    "ContentType": "application/json",
                }
                get_params = {
                    "Safe": self.params['Safe'],
                    "Keywords": self.params['Object'],
                }
                rcode, resp = self.get(account_url, headers=headers, params=get_params)
                respJSON = resp.json()
                account = respJSON['accounts'][0]
                self.vault_method = "EPV"
                self.vault = EPVResponse(account, auth_token=self.auth_token)
                self.is_valid = True
            except:
                raise

    def getCCPBaseUrl(self):
        return self.ccp_base_url

    def getEPVLogonUrl(self):
        return self.epv_logon_url

    def getEPVBaseUrl(self):
        return self.epv_base_url

    def setCCPBaseUrl(self, url):
        self.ccp_base_url = url

    def setEPVBaseUrl(self, url):
        self.epv_base_url = url

    def setEPVLogonUrl(self, url):
        self.epv_logon_url = url

    def setCAAppid(self, ca_appid):
        if ca_appid is not None:
            self.ca_appid = quote(ca_appid)
            return True
        else:
            return False

    def setCASafe(self, ca_safe):
        if ca_safe is not None:
            self.ca_safe = quote(ca_safe)
            return True
        else:
            return False

    def setCAObject(self, ca_object):
        if ca_object is not None:
            self.ca_object = quote(ca_object)
            return True
        else:
            return False

    #endregion: public interfaces

def main():
    pass

if __name__=="__main__":
    pass
