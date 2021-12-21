from __future__ import (print_function, unicode_literals, division)
__metaclass__ = type
import sys
try:
    import six
except ImportError:
    print("[*] Consider install python library six for more functionality. Trying to detect python version")
    six = lambda: None
    v = sys.version[0]
    if v == '3':
        six.PY3 = True
    elif v == '2':
        six.PY2 = True

if six.PY2:
    import BaseHTTPServer, SimpleHTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler

import ssl
keyfile='/etc/ssl/private/snakeoil.key'
certfile='/etc/ssl/certificates/snakeoil.pem'

ip = '0.0.0.0'
port = 8443
print("[*] Opening socket: %s:%s" % (ip, port))
httpd = BaseHTTPServer.HTTPServer( (ip, port),
            SimpleHTTPServer.SimpleHTTPRequestHandler
        )
try:
    httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile=keyfile,
        certfile=certfile,
        server_side=True
    )
    httpd.serve_forever()
except IOError:
    print("[!]: Unable to open TLS files: (%s)" % [keyfile, certfile])
