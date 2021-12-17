#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

## Standard Libraries
import os
import sys
from pprint import pprint,pformat
from configparser import ConfigParser as cfgparser

## Modules
from .BuildingBlocks import State               #pylint: disable=relative-beyond-top-level
from .BuildingBlocks import BaseObject          #pylint: disable=relative-beyond-top-level

class Manifest(BaseObject):

    def __init__(self, file=None):
        if file == None:
            raise AssertionError("Unable to successfully instantiate object of class::"+self.__class__.__name__)

        self.config_file = file
        config = self.config_parser = cfgparser()
        config.read(file)

        if 'qradar' in config:
            self.setReferenceSetName(config['qradar']['reference_set_name'])
        if 'ldap' in config:
            self.setLDAPQueryName(config['ldap']['query_name'])
            self.setLDAPQueryDefinition(config['ldap']['query_definition'])

        self.validate()
        self.ready(throw=True)

    def validate(self):
        self.is_valid = False
        if self.getLDAPQueryName() == None:
            return False
        if self.getLDAPQueryDefinition() == None:
            return False
        self.is_valid = True
        return True

    def setLDAPQueryName(self, val):
        self.ldap_query_name = val

    def setLDAPQueryDefinition(self, val):
        self.ldap_query_definition = val

    def getLDAPQueryName(self):
        try:
            return self.ldap_query_name
        except AttributeError:
            return None

    def getLDAPQueryDefinition(self):
        try:
            return self.ldap_query_definition
        except AttributeError:
            return None

    # The standard tuple is returned as such
    # ldap_named_search is mapped to ldap_query
    def getTuple(self):
        return(self.ldap_query_name, self.ldap_query_definition)

    def getTupleViaOrder(self, x, y):
        import copy

        ## Define acceptable values
        acceptable_query_names = ['name', 'query_name', 'ldap_query_name']
        acceptable_query_definitions = ['query', 'query_definition', 'ldap_query_definition', 'ldap_query']
        acceptable = acceptable_query_names+acceptable_query_definitions

        ## Create two dicts for tracking
        validation = {
            "getLDAPQueryName": acceptable_query_names,
            "getLDAPQueryDefinition": acceptable_query_definitions,
        }
        spare = copy.deepcopy(validation)

        # valN is used to return the tuple
        val1 = val2 = None

        # Validate x variable
        for fun,lis in validation.items():
            if x in lis:
                val1 = getattr(self, fun)()
                del spare[fun]
        if val1 == None:
            raise ValueError("x was not an appropriate value: use one of %s" % str(acceptable) )
        validation = copy.deepcopy(spare)

        # Validate y variable
        for fun,lis in validation.items():
            if y in lis:
                val2 = getattr(self, fun)()
                del spare[fun]
        if val2 == None:
            raise ValueError("y was not an appropriate value: use one of %s" % str(acceptable) )
        return (val1, val2)
