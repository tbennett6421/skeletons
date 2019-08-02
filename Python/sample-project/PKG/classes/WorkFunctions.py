import json

# Third-Party Libraries
import dns.resolver
from ldap3 import Server as LDAPServer
from ldap3 import ServerPool as LDAPServerPool
from ldap3 import Connection as LDAPConnection
from ldap3 import ALL,ROUND_ROBIN
from ldap3 import AUTO_BIND_TLS_BEFORE_BIND

## Modules
from .BuildingBlocks import State               #pylint: disable=relative-beyond-top-level

## Given a domain, return a list of domain controllers from DNS
def getDomainControllers(domain='google.com'):
    try:
        pg_state = State()
        args = pg_state.args
    except:
        pg_state = lambda: None
        args = lambda: None
        args.verbose = 0

    dcs = pg_state.domain_controllers = []
    srv_records = dns.resolver.query('_ldap._tcp.dc._msdcs.'+domain, 'SRV')
    for srv in srv_records:
        target = str(srv.target).rstrip('.')
        i = target.find(domain)
        h = target[:i].rstrip('.')
        dc = h.upper()+"."+domain
        dcs.append(dc)
        if args.verbose > 1:
            print("[**] DNS Response returned DC: %s" % (str(dc)))
    if args.verbose > 1: print()
    return dcs

## Given servers, return a connection object
def setupLDAPConnection(servers, bind_dn, bind_pass):
    try:
        pg_state = State()
        args = pg_state.args
    except:
        pg_state = lambda: None
        args = lambda: None
        args.verbose = 0

    if args.verbose:
        print("[*] Creating LDAPPool")
        if args.verbose > 1:
            print("[**] Building LDAPServerPool Object: (servers=None, pool_strategy=ROUND_ROBIN, active=True, exhaust=True)")
    LDAPPool = LDAPServerPool(servers=None, pool_strategy=ROUND_ROBIN, active=True, exhaust=True)
    for dc in servers:
        s = LDAPServer("ldaps://"+dc+":636", use_ssl=True, get_info=ALL)
        LDAPPool.add(s)
        if args.verbose > 1:
            print("[**] Constructed LDAPServer Object: (%s, use_ssl=True, get_info=ALL) and added to pool" % (str("ldaps://"+dc+":636")))
    if args.verbose > 1: print()
    if args.verbose:
        print("[*] Creating LDAPConnection")
    LDAPConn = LDAPConnection(LDAPPool, bind_dn, bind_pass, auto_bind=True)
    return LDAPConn

## Given a connection object, the query name, and the ldap query,
## function executes query and returns resultset
def executeLDAPQuery(conn, search_base=None, name=None, query=None):
    try:
        pg_state = State()
        args = pg_state.args
    except:
        pg_state = lambda: None
        args = lambda: None
        args.verbose = 0

    if search_base == None or name == None or query == None:
        raise AssertionError("Not all required arguments were passed in")

    if args.verbose > 1:
        print("[**] Executing: Conn.search(search_base=%s, search_filter=%s, attributes=['*'])" % (str(search_base), str(query)) )
    conn.search(search_base=search_base, search_filter=query, attributes=['*'])
    if args.verbose > 1:
        print("[!] %s: %d" % (str(name), len(conn.entries)) )
        for item in conn.entries:
            print("[+] sAMAccountName: %s" % (str(item.sAMAccountName)) )
        print()
    return conn.entries

## Given an attribute and resultset, returns list of unique attributes
def extractSingleAttribute(attrib, results):
    rval = []
    for item in results:
        rval.append(str(getattr(item, attrib)))
    return rval
