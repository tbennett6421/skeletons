#!/usr/bin/env python3

from __future__ import print_function
from __future__ import absolute_import

__code_version__ = 'v2.1.1'

## Standard Libraries
from datetime import datetime
import logging
import logging.handlers
import json
from queue import Queue

## Modules
try:
    from classes.BuildingBlocks import BuildingBlocks
except ModuleNotFoundError:
    try:
        from .BuildingBlocks import BuildingBlocks
    except ImportError:
        from BuildingBlocks import BuildingBlocks

class Logger(BaseObject):
    # region: Logger
    def __init__(self, log_name=None, log_level=None, log_format=None, log_file=None, start=False):
        ## Call parent init
        super().__init__()

        ## build self instance
        self.is_valid = False
        self.logger = None                          #logging object
        self.log_name = None                        #lazy-loadable parameter
        self.log_level = None                       #lazy-loadable parameter
        self.log_format = None                      #lazy-loadable parameter
        self.simple_queue = None
        self.default_logging_name = __name__
        self.default_logging_level = "WARNING"
        self.default_logging_format = '%(asctime)-15s [%(levelname)s] (%(name)s) - %(message)s'
        self.default_logging_format_dictionary = {
            "DEBUG": '%(asctime)-15s [%(levelname)s] (%(name)s) - %(message)s',
            "ERROR": self.default_logging_format,
            "CRITICAL": self.default_logging_format,
            'WARN': self.default_logging_format,
            'WARNING': self.default_logging_format,
            'INFO': self.default_logging_format
        }
        self.acceptable_log_levels = self.default_logging_format_dictionary.keys()
        self.set_log_name(log_name)
        self.set_log_level(log_level)
        self.set_log_format(log_format)
        self.set_log_file(log_file)
        self.configure(log_name=log_name, log_level=log_level, log_format=log_format, log_file=log_file, start=start)

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
            self.log_format = log_format
            self.formatter = logging.Formatter(self.log_format)

    """ Method to set log_file """
    def set_log_file(self, log_file=None):
        self.log_file = log_file

    """ If class is lazy loaded; call configure with params """
    def configure(self, log_name=None, log_level=None, log_format=None, log_file=None, start=False):
        self.set_log_level(log_level)
        self.set_log_name(log_name)
        self.set_log_format(log_format)
        self.set_log_file(log_file)
        if start:
            self.start()

    def addStreamHandler(self, stream=None):
        sh = self.stream_handler = logging.StreamHandler(stream)
        sh.setFormatter(self.formatter)
        self.attach(sh)

    def addFileHandler(self, filename, mode='a', encoding=None, delay=False):
        return self.addWatchedFileHandler(filename, mode=mode, encoding=encoding, delay=delay)

    def addQueueHandler(self):
        if self.simple_queue is not None:
            return
        else:
            q = self.simple_queue = Queue()
            qh = self.queue_handler = logging.handlers.QueueHandler(q)
            qh.setFormatter(self.formatter)
            self.attach(qh)

    def addWatchedFileHandler(self, filename, mode='a', encoding=None, delay=False):
        """
            As Logrotate is in effect, we are no longer using the RotatingFileHandler
            according to the docs we should be using the WatchedFileHandler.
        """
        # logging.handlers.WatchedFileHandler: pinned to 3.6.8
        fh = self.file_handler = logging.handlers.WatchedFileHandler(filename, mode=mode, encoding=encoding, delay=False)
        fh.setFormatter(self.formatter)
        self.attach(fh)

    def addRotatingFileHandler(self, filename, mode='a', encoding=None, delay=False, maxBytes=20000000, backupCount=5):
        """ Default to 5 copies, of 20MB each """
        fh = self.file_handler = logging.handlers.RotatingFileHandler(filename, mode=mode, maxBytes=maxBytes, backupCount=backupCount)
        fh.setFormatter(self.formatter)
        self.attach(fh)

    def getAllLogs(self):
        if self.simple_queue is None:
            return False
        else:
            lst = []
            while not self.simple_queue.empty():
                lst.append(self.simple_queue.get().message)
            return lst

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
            self.logger.setLevel(level=getattr(logging, self.log_level))
            self.addStreamHandler()
            self.log(msg="Logger ready", level=self.log_level)
            self.log(msg="Subscribed to %s level log channel" % (self.log_level), level=self.log_level)
            if self.log_file is not None:
                self.addFileHandler(self.log_file)
            if self.simple_queue is None:
                self.addQueueHandler()
            self.is_valid = True

    def log(self, message=None, msg=None, kwargs=None, level='Info'):
        b = self.check_log_level(level)
        if not b:
            return False
        # accept message or msg as message
        message = message if message else msg
        level = getattr(logging, level.upper())

        message = self.wrap_message_in_quotes(message)
        if kwargs:
            kwargs = self.handle_kwargs(kwargs)
            message = str(kwargs)+" "+message
            message = message.strip()
        return self.logger.log(msg=message, level=level)

    def handle_kwargs(self, kwargs):
        try:
            return '{0}'.format(' '.join(('{0}={1}'.format(k, v) for k, v in kwargs.items())))
        except AttributeError:
            return ""

    def wrap_message_in_quotes(self, message):
        if type(message) is list:
            if len(message) == 0:
                message = ""
            elif len(message) == 1:
                message = str(message)
            else:
                message = str("\n".join(message))
        else:
            message = str(message)
        return '"' + message + '"'

    def debug(self, message, kwargs=None):
        level='debug'
        self.log(msg=str(message), kwargs=kwargs, level=level)

    def error(self, message, kwargs=None):
        level='error'
        self.log(msg=str(message), kwargs=kwargs, level=level)

    def critical(self, message, kwargs=None):
        level='critical'
        self.log(msg=message, kwargs=kwargs, level=level)

    def warn(self, message, kwargs=None):
        level='warning'
        self.log(msg=str(message), kwargs=kwargs, level=level)

    def warning(self, message, kwargs=None):
        level='warning'
        self.log(msg=str(message), kwargs=kwargs, level=level)

    def info(self, message, kwargs=None):
        level='info'
        self.log(msg=str(message), kwargs=kwargs, level=level)

    # endregion: Logger

class SplunkLogger(Logger):
    # region: SplunkLogger

    def __init__(self, log_name=None, log_level=None, log_format=None, log_file=None, start=False):

        self.default_logging_format = '%(message)s'
        if log_name is None:
            log_name = 'splunk::'+__name__
        if log_level is None:
            log_level = 'WARN'
        if log_format is None:
            log_format = self.default_logging_format
        if log_file is None:
            raise AssertionError("SplunkLogger requires a log_file to emit logs")
        #self.splunk_keys = None

        ## Call parent init
        super().__init__(log_name=log_name, log_level=log_level, log_format=log_format, log_file=log_file, start=start)

    """ @overload: All logging mechanisms call .log() on the backend. Ignore kwargs but accept the parameter """
    def log(self, message=None, msg=None, kwargs=None, level='Info'):
        b = self.check_log_level(level)
        if not b:
            return False
        # accept message or msg as message
        message = message if message else msg
        level = getattr(logging, level.upper())
        return self.logger.log(msg=message, level=level)

    """ @overload: Do not start stream handlers """
    def start(self):
        if self.ready():
            return
        else:
            self.logger = logging.getLogger(self.log_name)
            self.logger.setLevel(level=getattr(logging, self.log_level))
            self.addQueueHandler()
            if self.log_file is not None:
                self.addFileHandler(self.log_file)
            if self.simple_queue is None:
                self.addQueueHandler()
            self.is_valid = True

    # endregion: SplunkLogger

class StructuredMessage():
    # region: StructuredMessage
    def __init__(self, message=None, msg=None, kw=None, **kwargs):
        # accept message or msg as message
        message = message if message else msg
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if kw is None:
            self.kwargs = kwargs
        else:
            self.kwargs = kw
        self.message = message
        self.kwargs['message'] = message
        self.kwargs['timestamp'] = ts
        self.msg = json.dumps(self.kwargs)

    def __str__(self):
        return '%s' % (self.msg)

    # endregion: StructuredMessage

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
