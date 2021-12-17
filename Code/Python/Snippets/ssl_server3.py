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
