__code_desc__ = "Put a description here"
__code_version__ = 'v0.0.0'
__code_debug__ = False
__code_color_support__ = True

## Standard Libraries
import os
import sys
import logging
import argparse

# Third Party libraries
if __code_color_support__:
    try:
        import colorama
        from termcolor import colored
    except ImportError:
        __code_color_support__ = False

# Modules

def print_console(msg, marker="[?]", fg_color=None, bg_color=None):
    f_str = f"{marker} {msg}"
    if __code_color_support__:
        print(colored(f_str, fg_color, bg_color))
    else:
        print(f_str)

def print_verbose(msg, marker='[*]'):
    print_console(msg,marker, fg_color='cyan')

def print_info(msg, marker='[+]'):
    print_console(msg,marker, fg_color='green')

def print_error(msg, marker='[!]'):
    print_console(msg,marker, fg_color='white', bg_color='on_red')

def init_colors(b=True):
    if b:
        colorama.init()
    else:
        global __code_color_support__
        __code_color_support__ = False

def begin_logging():
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
    parser = argparse.ArgumentParser(description=__code_desc__,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-V', '--version', action='version', version=__code_version__)
    parser.add_argument('-v', '--verbose', action='count', default=0)
    parser.add_argument('--disable-color', action='store_true',
        help='disable colorized output (you monster))')
    args = parser.parse_args()
    return parser, args

def handle_args():
    # collect parser if needed to conditionally call usage: parser.print_help()
    parser, args = collect_args()

    # negate args.disable_color; init_colors if needed
    init_colors(not args.disable_color)

    return parser, args

def main():
    log = begin_logging()
    parser, args = handle_args()

if __name__=="__main__":
    main()
