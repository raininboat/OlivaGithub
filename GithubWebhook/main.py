import OlivOS
import GithubWebhook
import os

logger = print

class Event(object):
    def init(plugin_event, Proc):
        global logger
        logger = LogWrapper(Proc.log)
        GithubWebhook.conf.load_data()

    def init_after(plugin_event, Proc):
        GithubWebhook.server.run_server()

    def save(plugin_event, Proc):
        pass

class LogWrapper:
    def __init__(self, proc_log):
        self.log = proc_log

    def trace(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(-1, str(msg).format(*args,**kwargs))
        else:
            self.log(-1, str(msg))

    def debug(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(0, str(msg).format(*args,**kwargs))
        else:
            self.log(0, str(msg))

    def note(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(1, str(msg).format(*args,**kwargs))
        else:
            self.log(1, str(msg))

    def info(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(2, str(msg).format(*args,**kwargs))
        else:
            self.log(2, str(msg))

    def warn(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(3, str(msg).format(*args,**kwargs))
        else:
            self.log(3, str(msg))

    def error(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(4, str(msg).format(*args,**kwargs))
        else:
            self.log(4, str(msg))

    def fatal(self, msg, *args, **kwargs):
        if args or kwargs:
            self.log(5, str(msg).format(*args,**kwargs))
        else:
            self.log(5, str(msg))

    def __call__(self, *args, **kwds):
        self.log(*args, **kwds)
