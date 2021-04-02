#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

__code_version__ = 'v1.0.4'

## Standard Libraries
import os
from urllib.parse import quote
from getpass import getpass

## Third-Party
import requests
from requests.models import HTTPError
import urllib3

## Modules
try:
    from .BuildingBlocks import BaseObject
except ImportError:
    from BuildingBlocks import BaseObject

class CyberArk(BaseObject):

    def __init__(self, ca_appid=None, ca_safe=None, ca_object=None, base_url="https://ccp.availity.net/AIMWebService/api/Accounts"):
        ## Call parent init
        super().__init__()

        # disable warnings is required due to requests bundling their own copy
        # of urllib3 and not passing tls_bundle down to the connection pool
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Configure TLS validation within requests
        self.configureTLSValidation()
        self.token = None
        self.is_valid = False
        self.base_url = base_url
        self.setCAParams(ca_appid, ca_safe, ca_object)

    def configureTLSValidation(self):
        try:
            self.tls_bundle = os.environ["REQUESTS_CA_BUNDLE"]
            self.verify = True
        except KeyError:
            RHEL_bundle = "/etc/pki/tls/certs/ca-bundle.crt"
            WSL_bundle = "/etc/ssl/certs/ca-certificates.crt"
            if os.path.isfile(RHEL_bundle):
                self.verify = True
                self.tls_bundle = RHEL_bundle
            elif os.path.isfile(WSL_bundle):
                self.verify = True
                self.tls_bundle = WSL_bundle
            else:
                self.verify = False
                self.tls_bundle = False

    def validate(self):
        if self.ca_appid is None:
            self.is_valid = False
            return False
        elif self.ca_safe is None:
            self.is_valid = False
            return False
        elif self.ca_object is None:
            self.is_valid = False
            return False
        else:
            self.is_valid = True
            return True

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

    def setCAParams(self, ca_appid=None, ca_safe=None, ca_object=None):
        self.setCAAppid(ca_appid)      #pylint: disable=not-callable
        self.setCASafe(ca_safe)        #pylint: disable=not-callable
        self.setCAObject(ca_object)    #pylint: disable=not-callable

    def buildParams(self):
        return {
            'AppId': self.ca_appid,
            'Safe': self.ca_safe,
            'Object': self.ca_object
        }

    """ doRequest uses the CCP endpoint to authenticate against cyberark using a trusted IP. """
    def doRequest(self):
        if self.validate():
            try:
                self.params = self.buildParams()
                r = requests.get(self.base_url, params=self.params, verify=self.tls_bundle)
                r.raise_for_status()
                self.request_object = r
                self.request_url = r.url
                self.request_responseText = r.text
                self.request_responseJSON = r.json()
                self.is_valid = True
                # at this point we should either have thrown httperror or not.
                # set attributes if we have not thrown httperror
                self.setName(name=self.CCPGetName(self.request_responseJSON))
                self.setUsername(username=self.CCPGetUsername(self.request_responseJSON))
                self.setPassword(password=self.CCPGetPassword(self.request_responseJSON))
            except HTTPError:
                self.doRequestUserFallback()
            except Exception:
                raise
        else:
            raise ValueError("Failed self.validate()")

    """
      doRequestUserFallback is used to authenticate to epv and pull creds
      for instance, when operating from a developer workstation.
    """
    def doRequestUserFallback(self):
        if not self.token:
            usernm = input("Cyberark Username: ")
            passwd = getpass("Cyberark Password: ")
            self.token = self.authenticateUser(username=usernm, password=passwd)
        if self.validate():
            try:
                account_url = "https://epv.availity.net/PasswordVault/WebServices/PIMServices.svc/Accounts"
                self.params = self.buildParams()
                headers = {
                    "Accept": "application/json",
                    "Authorization": self.token,
                    "ContentType": "application/json",
                }
                get_params = {
                    "Safe": self.params['Safe'],
                    "Keywords": self.params['Object'],
                }
                r = requests.get(account_url, headers=headers, params=get_params, verify=self.tls_bundle)
                r.raise_for_status()
                self.request_object = r
                self.request_url = r.url
                self.request_responseText = r.text
                self.request_responseJSON = r.json()
                self.is_valid = True
                # at this point we should either have thrown httperror or not.
                # set attributes if we have not thrown httperror
                self.setName(name=self.EPVGetName(self.request_responseJSON))
                self.setUsername(username=self.EPVGetUsername(self.request_responseJSON))
                self.setPassword(password=self.EPVGetPassword(self.request_responseJSON))
            except:
                raise
        else:
            raise ValueError("Failed self.validate()")

    def authenticateUser(self, username, password, logon_url="https://epv.availity.net/PasswordVault/WebServices/auth/Cyberark/CyberArkAuthenticationService.svc/Logon"):
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
        print("Making POST request to logon: %s" % (logon_url))
        print("Check MS Authenticator for MFA response")
        r = requests.post(logon_url, headers=headers, json=body, verify=self.tls_bundle)
        r.raise_for_status()
        respJson = r.json()
        return respJson['CyberArkLogonResult']

    def CCPGetName(self, response):
        try:
            return response['Name']
        except KeyError:
            return None

    def CCPGetUsername(self, response):
        try:
            return response['UserName']
        except KeyError:
            return None

    def CCPGetPassword(self, response):
        try:
            return response['Content']
        except KeyError:
            return None

    def EPVGetName(self, response):
        try:
            baseattribs = response['accounts'][0]['Properties']
            for item in baseattribs:
                if item['Key'] == "Name":
                    return item["Value"]
        except KeyError:
            return None

    def EPVGetUsername(self, response):
        try:
            baseattribs = response['accounts'][0]['Properties']
            for item in baseattribs:
                if item['Key'] == "UserName":
                    return item["Value"]
        except KeyError:
            return None

    def EPVGetPassword(self, response):
        # Get AccountID
        aid = response['accounts'][0]['AccountID']
        try:
            password_url = "https://epv.availity.net/PasswordVault/WebServices/PIMServices.svc/Accounts/%s/Credentials" % (aid)
            headers = {
                "Authorization": self.token,
            }
            r = requests.get(password_url, headers=headers, verify=self.tls_bundle)
            r.raise_for_status()
            self.password = r.text
            return self.password
        except:
            raise

    """
      set name manually or try from ccp response or try from epv response.
    """
    def setName(self, name=None):
        self.name = name

    def setUsername(self, username=None):
        self.username = username

    def setPassword(self, password=None):
        self.password = password

    def getName(self, throw=True):
        try:
            return self.name
        except Exception:
            if throw:
                raise
            else:
                return None

    def getUsername(self, throw=True):
        try:
            return self.username
        except Exception:
            if throw:
                raise
            else:
                return None

    def getPassword(self, throw=True):
        try:
            return self.password
        except Exception:
            if throw:
                raise
            else:
                return None

def demo():
    print("=== Demo ===")
    print("# Lazy loading CyberArk class")
    print(">>> ca = CyberArk()")
    print(">>> ca.ready()")
    ca = CyberArk()
    print(ca.ready())
    print(">>> ca.setCAAppid = 'CTF_APPS'")
    print(">>> ca.setCASafe = 'CTF_SECRETS'")
    print(">>> ca.setCAObject = 'dc1.krbtgt.hash'")
    ca.setCAAppid = "CTF_APPS"
    ca.setCASafe = "CTF_SECRETS"
    ca.setCAObject = "dc1.krbtgt.hash"
    print(">>> ca.ready()")
    print(ca.ready())

    print()
    print("# If the parameters set are valid and cyberark will successfully fulfil")
    print("# the request, you could call ca.doRequest() which would set ca.ready() to true")
    print("# Following a successful doRequest(), you can request the json parameters back from the object like so")
    print(">>> if ca.ready() is True:")
    print("...   username = ca.getUsername()")
    print("...   password = ca.getPassword()")
    print("...")

    print()
    print("# You can also request more then one secret. The following is an example")
    print("# of requesting five different secrets from a given safe. Using the same appid and safe as above")
    print(">>> ca_requests = ['dc1.localadmin', 'dc2.localadmin', 'wks1.localadmin', 'wks2.localadmin', 'kali.localadmin']")
    print(">>> login_creds = []")
    print(">>> for req in ca_requests:")
    print("...   ca.setCAObject = req")
    print("...   ca.doRequest()")
    print("...   if ca.ready() is True:")
    print("...      cred = ca.getName()")
    print("...      username = ca.getUsername()")
    print("...      password = ca.getPassword()")
    print("...      login_creds.append({username: password}) ")
    print("...")

def main():
    demo()

if __name__=="__main__":
    main()
