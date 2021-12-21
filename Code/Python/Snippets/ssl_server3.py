"""
    Features to-do:
        - implement argparse
        - use argparse to read TLS primitivates
        - use os.environment to read TLS primitives
        - when all else fails, hot-gen self-signed and use.
        - Make it look less ugly
        - Package and implement classes
"""

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
    from BaseHTTPServer import HTTPServer
    import BaseHTTPServer, SimpleHTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    get_input = raw_input
    class InterruptedError(KeyboardInterrupt):
        pass
else:
    from http.server import HTTPServer,SimpleHTTPRequestHandler
    get_input = input

import ssl
tls_primitives = {
    '/etc/ssl/private/snakeoil.key': '/etc/ssl/certificates/snakeoil.pem',
    'key.pem': 'cert.pem'
}

ip = '0.0.0.0'
port = 8443
socket = (ip, port)
print("[*] Opening socket: %s:%s" % (socket))
httpd = HTTPServer(socket, SimpleHTTPRequestHandler)

for key,cert in tls_primitives.items():
    try:
        print("[?] Attempting to wrap socket in TLS via: %s:%s" % (key, cert))
        httpd.socket = ssl.wrap_socket (httpd.socket,
            keyfile=key,
            certfile=cert,
            server_side=True
        )
        while True:
            try:
                print("[*] Serving: %s:%s" % (ip, port))
                httpd.serve_forever()
            except KeyboardInterrupt as e:
                msg="\n[!]: Caught ctrl+c: Do you wish to exit?: "
                choice=get_input(msg)
                if str(choice).lower()[0] == 'y':
                    raise InterruptedError
                else:
                    pass
    except InterruptedError:
        msg="[!]: Exit requested"
        print(msg)
    except KeyboardInterrupt:
        msg="\n[!]: Caught ctrl+c twice: Forcing shutdown"
        print(msg)
    except IOError:
        print("[!]: Unable to open TLS files: (%s)" % [key, cert])
