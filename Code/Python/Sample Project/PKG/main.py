#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

__code_version__ = 'v0.0.1'
__code_desc__ = """
program description to be displayed by argparse
    ex: python {name}
""".format(name=__file__)

# Standard Libraries
import os
import sys
import argparse
from pprint import pprint,pformat
from copy import deepcopy as deepcopy

# Third-Party Libraries
import ldap3
import requests
import cx_Oracle

# Modules
from classes.BuildingBlocks import State                    #pylint: disable=import-error,no-name-in-module
from classes.Manifest import Manifest                       #pylint: disable=import-error,no-name-in-module
from classes.WorkFunctions import getDomainControllers      #pylint: disable=import-error,no-name-in-module
from classes.WorkFunctions import setupLDAPConnection       #pylint: disable=import-error,no-name-in-module
from classes.WorkFunctions import executeLDAPQuery          #pylint: disable=import-error,no-name-in-module
from classes.ErrorFunctions import handleBacktrace          #pylint: disable=import-error,no-name-in-module

def init():
    ## import program state
    pg_state = State()

    #region BuildArgParser
    parser = argparse.ArgumentParser(description=__code_desc__)
    parser.add_argument('-V','--version', action='version', version='%(prog)s '+__code_version__)
    parser.add_argument('-v','--verbose', action='count', default=0, help="Print verbose output to the console. Multiple v's increase verbosity")
    parser.add_argument('--debug', action='store_true', help="Toggle debugging output to the console.")
    args = parser.parse_args()
    pg_state.args = args
    #endregion

    # Build some manifests
    pg_state.manifests = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    man_path = os.path.join(dir_path, "manifests")
    for file in os.listdir(man_path):
        if file.endswith(".ini"):
            pg_state.manifests.append(Manifest(os.path.join(man_path,file)))

    #region InitLDAP
    if args.verbose:
        print("[*] Setting LDAP parameters")
    pg_state.domain_name = "google.com"
    pg_state.ldap_root = "DC=google,DC=com"
    pg_state.bind_dn = "CN=ldapbind,OU=Service Accounts,DC=google,DC=com"
    pg_state.bind_pass = None #pylint: disable=no-member
    if args.verbose > 1:
        print("[**] Set pg_state.domain_name: %s" % (str(pg_state.domain_name)))
        print("[**] Set pg_state.ldap_root: %s" % (str(pg_state.ldap_root)))
        print("[**] Set pg_state.bind_dn: %s" % (str(pg_state.bind_dn)))
        print("[**] Fetch/Set pg_state.bind_pass: %s" % ("<redacted>"))
    #endregion

def main():
    init()
    pg_state = State()
    args = pg_state.args

    try:

        ## Fetch Domain Controllers
        if args.verbose:
            print("[*] Fetching domain controllers via SRV lookup")
        dcs = pg_state.domain_controllers = getDomainControllers(domain=pg_state.domain_name)

        ## Setup LDAP Connection
        LDAPConn = pg_state.LDAPConn = setupLDAPConnection(dcs, pg_state.bind_dn, pg_state.bind_pass)
        pg_state.LDAPPool = pg_state.LDAPConn.server_pool
        pg_state.LDAPServers = pg_state.LDAPPool.servers

        ## Execute LDAP Queries
        if args.verbose:
            print("[*] Unpacking manifests and executing queries against LDAP")
            print()

        for manifest in pg_state.manifests:
            ## Unpack manifest
            ldap_query_name, ldap_query_definition = manifest.getTuple() #pylint: disable=no-member
            if args.verbose > 1:
                print("[**] Unpacked a manifest")
                print("[**] Set ldap_query_name: %s" % (str(ldap_query_name)))
                print("[**] Set ldap_query_definition: %s" % (str(ldap_query_definition)))
                print()

            ## run ldap query
            resultSet = executeLDAPQuery(conn=LDAPConn, search_base=pg_state.ldap_root, name=ldap_query_name, query=ldap_query_definition)
            ## Get all accounts and set aside
            accounts = extractSingleAttribute("sAMAccountName", resultSet) #pylint: disable=undefined-variable
            accounts = [item.lower() for item in accounts]
            if args.verbose > 2:
                print("[***] Extracting sAMAccountName from resultSet")
                print("[***] Dropping values to lowercase")
                print()

    except Exception as e:
        if args.debug:
            print("[<>] Caught Exception for handling")
            print("[<>] Cloning Stack")
            stack = deepcopy(locals())
            handleBacktrace(stack)
        else:
            raise


if __name__=="__main__":
    main()
