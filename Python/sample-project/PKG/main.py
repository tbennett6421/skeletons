#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

__code_version__ = 'v0.0.1'
__code_desc__ = """
program description to be displayed by argparse
    ex: python {name}
""".format(name=__file__)

# Standard Libraries
import argparse
from pprint import pprint,pformat

# Third-Party Libraries

# Modules
from classes.BuildingBlocks import State                    #pylint: disable=import-error,no-name-in-module
from classes.Manifest import Manifest                       #pylint: disable=import-error,no-name-in-module

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



if __name__=="__main__":
    main()
