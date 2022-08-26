#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

__code_version__ = 'v1.1.1'

## Standard Libraries
import os

## Third-Party
import cx_Oracle

## Modules
try:
    from classes.BuildingBlocks import BaseObject
    from classes.CyberArk import CyberArk
except ModuleNotFoundError:
    try:
        from .BuildingBlocks import BaseObject
        from .CyberArk import CyberArk
    except ImportError:
        from BuildingBlocks import BaseObject
        from CyberArk import CyberArk

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
        except KeyError:
            return None

    def getDBUsername(self):
        try:
            return self.db_username
        except KeyError:
            return None

    def getDBPassword(self):
        try:
            return self.db_password
        except KeyError:
            return None

    def getDBHost(self):
        try:
            return self.db_host
        except KeyError:
            return None

    def getDBPort(self):
        try:
            return self.db_port
        except KeyError:
            return None

    def getDBSID(self):
        try:
            return self.db_sid
        except KeyError:
            return None

    def getDBConnectString(self):
        try:
            return self.db_connect_string
        except KeyError:
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

class AvailityOracle(Oracle):

    def __init__(self):
        ## Call parent init()
        super().__init__()
        self.krb_strings = {
            "tracker": "/@track.prd",
        }
        ## Keep track of initial auth, allows switching functions to work without re-setting up the authentication
        self.authenticated_successfully = False

    def auth(self, method='kerberos', host=None, port=1521, username=None, password=None, sid=None, connect_string=None, cached=False,):
        # Calling self.login, or self.SSOLogin both persist authentication variables to self, using a cached
        # flag we can restore frame parameters using self
        if cached is True:
            method = self.getDBAuthMethod()
            host = self.getDBHost()
            port = self.getDBPort()
            username = self.getDBUsername()
            password = self.getDBPassword()
            sid = self.getDBSID()
            connect_string = self.getDBConnectString()
        else:
            method = self.db_auth_method = method.lower() #pylint: disable=no-member
            acceptable_auth_methods = ['kerberos', 'basic']
            if method not in acceptable_auth_methods:
                raise ValueError(str(method)+" not in "+acceptable_auth_methods)

        if method == "kerberos":
            self.SSOLogin(connect_string=connect_string)
            self.authenticated_successfully = True
        if method == "basic":
            self.login(host=host, port=port, username=username, password=password, sid=sid)
            self.authenticated_successfully = True

    """ Initialize stub for maltego svcprdsoctracker connections to Oracle """
    @classmethod
    def initializeATAdmin(self, db_auth='basic', db_host='gateway-scan.dt.prd.availity.net', db_port=1521, db_sid='aries_rpt.availity.net', ca_appid='APP_SOC_PRD', ca_safe='PRIV_SOC', ca_object='svcprdsoctracker', maltego_response_object=None, debug=False):
        if debug:
            from maltego_trx.maltego import UIM_INFORM
            assert maltego_response_object is not None
        # Setup the database params
        cyberark_object = CyberArk(
            ca_appid=ca_appid,
            ca_safe=ca_safe,
            ca_object=ca_object
        )
        cyberark_object.doRequest()
        if debug:
            maltego_response_object.addUIMessage("CyberArk App ID: %s" % (str(ca_appid)), UIM_INFORM )
            maltego_response_object.addUIMessage("CyberArk Safe: %s" % (str(ca_safe)), UIM_INFORM )
            maltego_response_object.addUIMessage("CyberArk Object: %s" % (str(ca_object)), UIM_INFORM )
            maltego_response_object.addUIMessage("CyberArk.ready()?: %s" % (str(cyberark_object.ready())), UIM_INFORM )
        # Setup the database params
        db_username = ca_object
        db_password = cyberark_object.getPassword()

        if debug:
            maltego_response_object.addUIMessage("Oracle DB Auth Mechanism: %s" % (str(db_auth)), UIM_INFORM )
            maltego_response_object.addUIMessage("Oracle DB Host: %s" % (str(db_host)), UIM_INFORM )
            maltego_response_object.addUIMessage("Oracle DB Port: %s" % (str(db_port)), UIM_INFORM )
            maltego_response_object.addUIMessage("Oracle DB SID: %s" % (str(db_sid)), UIM_INFORM )
            maltego_response_object.addUIMessage("Oracle DB Username: %s" % (str(db_username)), UIM_INFORM )

        # Setup the database object
        avo = AvailityOracle()
        avo.auth(method=db_auth, host=db_host, port=db_port, username=db_username, password=db_password, sid=db_sid)
        if debug:
            maltego_response_object.addUIMessage("AvailityOracle.ready()?: %s" % (str(avo.ready())), UIM_INFORM )
        return avo

    def getTrackerConnectString(self):
        return self.krb_strings['tracker']

    # dummy methods only support kerberos login at this time
    def selectTracker(self):
        if self.db_auth_method == 'kerberos':
            self.db_connect_string = self.getTrackerConnectString()
            self.auth(connect_string=self.db_connect_string, method=self.db_auth_method)
            return True
        else:
            return False

    #region comment
    # def fileToString(self, filename):
    #     # Changes a CSV or TXT to a single line of comma values.
    #      with open(filename, 'r') as myfile:
    #          if ('.txt' == str(filename[-4:])):
    #              fullString = "'" + str(myfile.read().replace('\n','\', \'')) + "'"
    #          if ('.csv' == str(filename[-4:])):
    #              fullString = "'" + str(myfile.read().replace(',','\',\'')) + "'"
    #      return fullString

    # def getUniqueReferenceIDs(self):
    #     columns = "REFERENCE_ID"
    #     table = "ATADMIN.VERIFICATION_REQUEST"
    #     query = "SELECT DISTINCT "+columns+" FROM "+table
    #     self.lastQuery = query
    #     self.lastResult = self.cursor.execute(self.lastQuery)
    #     self.lastRows = self.lastResult.fetchall()
    #     return list(set(self.lastRows))

    # def buildQuery(self, columns=None, table=None, method="single"):
    #     acceptable = ["single", "bulk"]
    #     if method not in acceptable:
    #         raise ValueError("Unknown method: "+str(method))

    #     columns = "REFERENCE_ID,IP_ADDRESS,TRANSACTION_STATUS,REQUEST_UI_URL, REQUEST_VENDOR_URL, RESPONSE_UI_URL, RESPONSE_VENDOR_URL"
    #     table = "ATADMIN.VERIFICATION_REQUEST"
    #     order = "reference_id asc"

    #     query = ""
    #     if method == "single":
    #         query = "SELECT "+columns+" FROM "+table+" WHERE reference_id = :param ORDER BY "+order
    #     if method == "bulk":
    #         query = "SELECT "+columns+" FROM "+table+" WHERE reference_id in :param ORDER BY "+order
    #     self.lastQuery = query
    #     return self.lastQuery

    ## build the query to gather CIDs from TINs
    # def buildTINQuery(self, tin):
    #     cid_column = "CUSTOMER_ID"
    #     table = "AV_DW.DIM_CUSTOMER"

    #     ## Get all records for a given tin
    #     self.lastQuery = "SELECT DISTINCT * FROM "+table+" WHERE tax_id = :param"
    #     result = self.doQuery(self.lastQuery, tin)
    #     num_rows = len(result)

    #     ## Gather CIDs and count
    #     cids = []

    #     for row in result:
    #         if row[cid_column] is not None:
    #            cids.append(row[cid_column])
    #     return num_rows, cids

    # def buildUserQuery(self, cid):
    #     cid_column = "CUSTOMER_ID"
    #     table = "AV_DW.DIM_USER"
    #     columns = "AKA_NM, FIRST_NM, LAST_NM, USER_STATUS, CUSTOMER_TO_USER_STATUS, USER_ID, EMAIL_ADDR"
    #     self.lastQuery = "SELECT "+columns+" FROM "+table+" WHERE "+cid_column+" = :param"
    #     result = self.doQuery(self.lastQuery, cid)
    #     num_rows = len(result)
    #     return num_rows, result
    #endregion comment

def demo():
    pass

def main():
    demo()

if __name__=="__main__":
    main()
