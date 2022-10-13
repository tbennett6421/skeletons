from __future__ import (print_function,absolute_import)

__code_desc__ = "Put a description here"
__code_version__ = 'v0.0.1'
__code_debug__ = False
__code_color_support__ = True
__code_vsc_support__ = True

## Standard Libraries
import os
import sys
import logging
from argparse import ArgumentParser, RawTextHelpFormatter
from pprint import pformat, pprint

## Third Party libraries
try:
    # Do we have what we need to use colors?
    import colorama
    from termcolor import colored
    __code_color_support__ = True
except ImportError:
    __code_color_support__ = False

try:
    # Do we have what we need to work with vscode
    import debugpy
    debugpy.listen(5678)
    debugpy.wait_for_client()
    __code_vsc_support__ = True
except (ImportError, SystemExit, RuntimeError) as e:
    __code_vsc_support__ = False

# Modules
# place content here

# Local functions
def print_console(msg, marker="[?]", fg_color=None, bg_color=None):
    f_str = f"{marker} {msg}"
    if __code_color_support__:
        print(colored(f_str, fg_color, bg_color))
    else:
        print(f_str)

def print_verbose(msg, marker='[*]'):
    print_console(msg, marker, fg_color='cyan')

def print_info(msg, marker='[+]'):
    print_console(msg, marker, fg_color='green')

def print_error(msg, marker='[!]'):
    print_console(msg, marker, fg_color='white', bg_color='on_red')

def init_colors(b=True):
    if b:
        colorama.init()
    else:
        __code_color_support__ = False

def begin_logging(debug=False):
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            style="{",
            fmt="[{name}:{filename}] {levelname} - {message}"
        )
    )
    log = logging.getLogger(__name__)
    if __code_debug__:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    log.addHandler(handler)
    return log

def collect_args():
    parser = ArgumentParser(description=__code_desc__,
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('-V', '--version', action='version', version=__code_version__)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--debug', action='store_true', help="Enable debugging")
    parser.add_argument('--disable-color', action='store_true',
        help='disable colorized output (you monster))')
    args = parser.parse_args()
    return parser, args

def handle_args():
    # collect parser if needed to conditionally call usage: parser.print_help()
    parser, args = collect_args()

    if args.debug:
        __code_debug__ = True

    # negate args.disable_color; init_colors if needed
    init_colors(not args.disable_color)

    return parser, args

def main():
    parser, args = handle_args()
    log = begin_logging(debug=__code_debug__)

if __name__=="__main__":
    main()
