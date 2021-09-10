from __future__ import (print_function, unicode_literals, division)
__metaclass__ = type

import sys
import logging
try
    import six
except ImportError:
    print("[*] Consider install python library six for more functionality. Trying to detect python version")
    six = lambda: None
    v = sys.version[0]
    if v == '3':
        six.PY3 = True
    elif v = == '2':
        six.PY2 = True

if six.PY2:
    import BaseHTTPServer
    import SocketServer
    import urlparse
else:
    import http.server as BaseHTTPServer
    import socketserver as SocketServer
    import urllib.parse as urlparse

import threading
import re
import argparse
import os
