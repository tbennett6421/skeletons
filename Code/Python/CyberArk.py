#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

## Standard Libraries
from pprint import pprint

## Third-Party
import requests
import urllib3
from urllib.parse import quote

## Modules
from .BuildingBlocks import State               #pylint: disable=relative-beyond-top-level
from .BuildingBlocks import BaseObject          #pylint: disable=relative-beyond-top-level

class CyberArk(BaseObject):

    def __init__(self, ca_appid=None, ca_safe=None, ca_object=None, base_url=None):
        ## Call parent init
        super().__init__()

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self.is_valid = False
        self.setCAParams(ca_appid, ca_safe, ca_object, base_url)

    def validate(self):
        self.is_valid = False
        if self.ca_appid is None:
            return False
        elif self.ca_safe is None:
            return False
        elif self.ca_object is None:
            return False
        elif self.base_url is None:
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

    def setCAServerUrl(self, base_url):
        if base_url is not None:
            self.base_url = base_url
            return True
        else:
            return False

    def setCAParams(self, ca_appid=None, ca_safe=None, ca_object=None, base_url=None):
        self.setCAAppid(ca_appid)           #pylint: disable=not-callable
        self.setCASafe(ca_safe)             #pylint: disable=not-callable
        self.setCAObject(ca_object)         #pylint: disable=not-callable
        self.setCAServerUrl(base_url)       #pylint: disable=not-callable

    def buildParams(self):
        return {
            'AppId': self.ca_appid,
            'Safe': self.ca_safe,
            'Object': self.ca_object
        }

    def doRequest(self):
        if self.validate() == True:
            try:
                self.params = self.buildParams()
                r = requests.get(self.base_url, params=self.params, verify=False)
                r.raise_for_status()
                self.request_object = r
                self.request_url = r.url
                self.request_responseText = r.text
                self.request_responseJSON = r.json()
                self.is_valid = True

                self.setName()
                self.setUsername()
                self.setPassword()
            except:
                raise
        else:
            raise ValueError("Failed self.validate()")

    def setName(self):
        self.name = self.request_responseJSON['Name']

    def setUsername(self):
        try:
            self.username = self.request_responseJSON['UserName']
        except KeyError:
            self.username = None

    def setPassword(self):
        self.password = self.request_responseJSON['Content']

    def getName(self, throw=True):
        try:
            return self.name
        except:
            if throw:
                raise
            else:
                return None

    def getUsername(self, throw=True):
        try:
            return self.username
        except:
            if throw:
                raise
            else:
                return None

    def getPassword(self, throw=True):
        try:
            return self.password
        except:
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
