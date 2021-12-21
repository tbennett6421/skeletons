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

import BaseHTTPServer, SimpleHTTPServer
import ssl

keyfile='/etc/ssl/private/snakeoil.key'
certfile='/etc/ssl/certificates/snakeoil.pem'

httpd = BaseHTTPServer.HTTPServer(('0.0.0.0', 443),
        SimpleHTTPServer.SimpleHTTPRequestHandler)

httpd.socket = ssl.wrap_socket (httpd.socket,
        keyfile=keyfile,
        certfile=certfile,
        server_side=True)

httpd.serve_forever()
