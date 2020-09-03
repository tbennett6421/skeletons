#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

## Standard Libraries
from pprint import pprint
import logging

## Modules
from .BuildingBlocks import State               #pylint: disable=relative-beyond-top-level
from .BuildingBlocks import BaseObject          #pylint: disable=relative-beyond-top-level

class Logger(BaseObject):

    def __init__(self, log_name=None, log_level=None, log_format=None, start=False):
        ## Call parent init
        super().__init__()

        ## build self instance
        self.is_valid = False
        self.logger = None                          #logging object
        self.log_name = None                        #lazy-loadable parameter
        self.log_level = None                       #lazy-loadable parameter
        self.log_format = None                      #lazy-loadable parameter
        self.default_logging_name = __name__
        self.default_logging_level = "WARNING"
        self.default_logging_format = '%(asctime)-15s %(levelname)s log_name=%(name)s log_module=%(module)s %(message)s'
        self.default_logging_format_dictionary = {
            "DEBUG": '%(asctime)-15s [%(levelname)s] (%(name)s) [%(module)s] %(funcName)s:%(lineno)d - %(message)s',
            'WARNING': self.default_logging_format,
            'WARN': self.default_logging_format,
            'INFO': self.default_logging_format
        }
        self.acceptable_log_levels = self.default_logging_format_dictionary.keys()
        self.set_log_name(log_name)
        self.set_log_level(log_level)
        self.set_log_format(log_format)
        if start:
            self.configure(log_name=log_name, log_level=log_level, log_format=log_format)
            self.start()

    """ Method to set log_name """
    def set_log_name(self, log_name=None):
        if log_name is None:
            self.log_name = self.default_logging_name
        else:
            self.log_name = log_name

    """ Method to validate log_level """
    def check_log_level(self, log_level):
        # check if acceptable
        log_level = str(log_level).upper()
        if log_level in self.acceptable_log_levels:
            return True
        else:
            return False

    """ Method to set log_level """
    def set_log_level(self, log_level=None):
        if log_level is None:
            self.log_level = self.default_logging_level
        else:
            log_level = str(log_level).upper()                  # cast to upper
            b = self.check_log_level(log_level)                 # check value
            if b:
                if log_level == "WARN": log_level = "WARNING"   # cast to correct name
                self.log_level = log_level
            else:
                self.log_level = self.default_logging_level

    """ Method to set log_format """
    def set_log_format(self, log_format):
        if log_format is None:
            if self.log_level is None:
                self.log_format = self.default_logging_format
                self.formatter = logging.Formatter(self.log_format)
            else:
                self.log_format = self.default_logging_format_dictionary[self.log_level]
                self.formatter = logging.Formatter(self.log_format)
        else:
            self.log_format = self.log_format
            self.formatter = logging.Formatter(self.log_format)

    """ If class is lazy loaded; call configure with params """
    def configure(self, log_name=None, log_level=None, log_format=None, start=False):
        self.set_log_level(log_level)
        self.set_log_name(log_name)
        self.set_log_format(log_format)

    def addStreamHandler(self, stream=None):
        sh = self.stream_handler = logging.StreamHandler(stream)
        sh.setFormatter(self.formatter)
        self.attach(sh)

    def addFileHandler(self, filename, mode='a', encoding=None, delay=False):
        fh = self.file_handler = logging.FileHandler(filename)
        fh.setFormatter(self.formatter)
        self.attach(fh)

    def attach(self, handler):
        if self.logger is None:
            print(">>> Unable to attach a handler to a non-started logger")
            print(">>> Starting the logger for you")
            self.start()
        self.logger.addHandler(handler)

    def start(self):
        if self.ready():
            return
        else: 
            self.logger = logging.getLogger(self.log_name)
            self.addStreamHandler()
            self.logger.setLevel(level=getattr(logging, self.log_level))
            self.log(msg="Logger ready", level=self.log_level)
            self.log(msg="Subscribed to %s level log channel" % (self.log_level), level=self.log_level)
            self.is_valid = True

    def log(self, message=None, msg=None, level='Info'):
        b = self.check_log_level(level)
        if not b:
            return False
        # accept message or msg as message
        message = message if message else msg
        level = getattr(logging, level.upper())
        return self.logger.log(msg=message, level=level)

    def handle_kwargs(self, kwargs):
        return '{0}'.format(' '.join(('{0}={1}'.format(k, v) for k, v in kwargs.items())))
        
    def wrap_message_in_quotes(self, message):
        if type(message) is list:
            if len(message) is 0:
                message = ""
            elif len(message) is 1:
                message = str(message)
            else:
                message = str("\n".join(message))
        else:
            message = str(message)
        return '"' + message + '"'

    def debug(self, message, kwargs=None):
        level='debug'
        message = self.wrap_message_in_quotes(message)
        if kwargs:
            kwargs = self.handle_kwargs(kwargs)
            message = kwargs+" "+message
        self.log(msg=message, level=level)
        
    def error(self, message, kwargs=None):
        level='error'
        message = self.wrap_message_in_quotes(message)
        if kwargs:
            kwargs = self.handle_kwargs(kwargs)
            message = kwargs+" "+message
        self.log(msg=message, level=level)

    def critical(self, message, kwargs=None):
        level='critical'
        message = self.wrap_message_in_quotes(message)
        if kwargs:
            kwargs = self.handle_kwargs(kwargs)
            message = kwargs+" "+message
        self.log(msg=message, level=level)

    def warn(self, message, kwargs=None):
        level='warning'
        message = self.wrap_message_in_quotes(message)
        if kwargs:
            kwargs = self.handle_kwargs(kwargs)
            message = kwargs+" "+message
        self.log(msg=message, level=level)

    def warning(self, message, kwargs=None):
        level='warning'
        message = self.wrap_message_in_quotes(message)
        if kwargs:
            kwargs = self.handle_kwargs(kwargs)
            message = kwargs+" "+message
        self.log(msg=message, level=level)

    def info(self, message, kwargs=None):
        level='info'
        message = self.wrap_message_in_quotes(message)
        if kwargs:
            kwargs = self.handle_kwargs(kwargs)
            message = kwargs+" "+message
        self.log(msg=message, level=level)

def demo():
    just_doit = Logger(start=True)
    just_doit.warn("Logging started with defaults")
    just_doit.warn("just_doit.ready() returns (%s)" % (just_doit.ready()) )

    normal_usage = Logger(log_name="my_application", log_level="info", start=True)
    normal_usage.info("Create logger using init()")

    lazy_loading = Logger()
    lazy_loading.set_log_level("debug")
    lazy_loading.set_log_name("my_app.debug")
    lazy_loading.addFileHandler("spam.log")
    lazy_loading.start()
    lazy_loading.critical("Fatal error logged")

def main():
    demo

if __name__=="__main__":
    main()
