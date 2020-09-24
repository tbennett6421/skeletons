#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

## Standard Libraries
import os
from pprint import pprint

## Third-Party
import cx_Oracle

## Modules
from .BuildingBlocks import State               #pylint: disable=relative-beyond-top-level
from .BuildingBlocks import BaseObject          #pylint: disable=relative-beyond-top-level

class Oracle(BaseObject):

    def __init__(self):
        ## Call parent init
        super().__init__()
        self.__init_vars__()
        self.setupEnvironment()
        self.db_auth_method = 'kerberos'

    def __init_vars__(self):
        self.db_connect_string = None
        self.db_username = None
        self.db_password = None
        self.db_host = None
        self.db_port = None
        self.db_sid = None
        self.db_auth_method = None

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except cx_Oracle.DatabaseError:
            pass
        except AttributeError:
            pass

    def setupEnvironment(self):
        ## Ensure library and Oracle Home are set
        ## not tested on systems where these are already set
        try:
            _ = os.environ["ORACLE_HOME"]
        except KeyError:
            os.environ["ORACLE_HOME"] = "/opt/oracle/64/product/12.1.0/client_1/"
        try:
            _ = os.environ["LD_LIBRARY_PATH"]
        except KeyError:
            os.environ["LD_LIBRARY_PATH"] = "/opt/oracle/64/product/12.1.0/client_1/lib"

    def rowfactoryAsDict(self, cursor):
        columnNames = [d[0] for d in cursor.description]
        def createRow(*args):
            return dict(zip(columnNames, args))
        return createRow
    
    def getDBAuthMethod(self):
        try:
            return self.db_auth_method
        except:
            return None
    
    def getDBUsername(self):
        try:
            return self.db_username
        except:
            return None
    
    def getDBPassword(self):
        try:
            return self.db_password
        except:
            return None

    def getDBHost(self):
        try:
            return self.db_host
        except:
            return None

    def getDBPort(self):
        try:
            return self.db_port
        except:
            return None

    def getDBSID(self):
        try:
            return self.db_sid
        except:
            return None

    def getDBConnectString(self):
        try:
            return self.db_connect_string
        except:
            return None

    def returnAuth(self):
        return {
            "db_connect_string": self.getDBConnectString(),
            "db_username": self.getDBUsername(),
            "db_password": self.getDBPassword(),
            "db_host": self.getDBHost(),
            "db_port": self.getDBPort(),
            "db_sid": self.getDBSID(),
            "db_auth_method": self.getDBAuthMethod(),
        }

    def SSOLogin(self, connect_string=None):
        """ use kerberos method, only requres a connect_string. (/@track.prd) """
        self.db_auth_method = "kerberos"
        if connect_string is None:
            raise ValueError("Param error: requires 'connect_string'")
        self.db_connect_string = connect_string
        try:
            self.conn = cx_Oracle.connect(self.db_connect_string)
            self.cursor = self.conn.cursor()
            self.is_valid = True
        except:
            raise

    def login(self, host=None, port=1521, username=None, password=None, sid=None):
        """ use basic method, requires user/pass and info to build a dsn """
        self.db_username = username
        self.db_password = password
        self.db_host = host
        self.db_port = port
        self.db_sid = sid
        self.db_auth_method = "basic"
        try:
            dsn = self.dsn = str(host) + ":" + str(port) + "/" + str(sid)
            self.conn = cx_Oracle.connect(username, password, dsn)
            self.cursor = self.conn.cursor()
            self.is_valid = True
        except:
            raise

    def connect(self):
        """ dummy method """
        return self.ready(throw=True, message="Unable to connect() without authenticating first")

    def prepare(self, name):
        return ":"+str(name)

    def prepareSelectStatement(self, distinct=None, columns='*', table=None, whereKey=None, whereVal=None, method="single"):
        """ Create a prepared SELECT statement and return query and prepared dictionary for execution """
        acceptable = ["single", ]#"bulk"]
        method = method.lower()
        if method not in acceptable:
            raise ValueError("Unknown method: "+str(method))
        prep = {}

        #region select
        query = "SELECT "
        if distinct is True:
            query = query + "DISTINCT "

        # convert to str
        if type(columns) is list:
            columns = ' '.join(columns)
        
        placeholder = "pCols"
        prep[placeholder] = columns
        query = query + self.prepare(placeholder) + " "

        placeholder = "pTable"
        prep[placeholder] = table        
        query = query + "FROM "+ self.prepare(placeholder) + " "
        #endregion select

        if whereKey is not None:
            placeholder = "pWhere"
            prep[placeholder] = whereKey
            if method == "single":
                query = query + "WHERE " + self.prepare(placeholder) + " = " + ":param "
            # if method == "bulk":
            #     query = query + "WHERE " + self.prepare(placeholder) + " in " + ":param "
            prep['param'] = whereVal

        self.lastQuery = query
        self.lastPrepDict = prep
        return query, prep

    def doQuery(self, query, prep):
        self.lastResult = self.cursor.execute(query, prep)
        self.lastResult.rowfactory = self.rowfactoryAsDict(self.lastResult)
        self.lastRows = self.lastResult.fetchall()
        return self.lastRows

def demo():
    pass

def main():
    demo()

if __name__=="__main__":
    main()
