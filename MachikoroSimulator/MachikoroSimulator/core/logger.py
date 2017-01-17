from enum import IntEnum


class Verbosity(IntEnum):
    Debug = 5,
    Info = 4,
    Warn = 3,
    Error = 2,
    Fatal = 1



class Logger:
    Levels = {Verbosity.Debug: "DEBUG", Verbosity.Info: "INFO ",
              Verbosity.Warn: "WARN ", Verbosity.Error: "ERROR",
              Verbosity.Fatal: "FATAL"}

    def __init__(self, verbosity=Verbosity.Debug, appender=None):
        #TODO: eventually I should make this configurable by .config file or something, like log4net or others.
        self._verbosity = verbosity
        if appender is None:
            appender = _default_appender
        self._appender = appender

    def _append(self, template, args):
        self._appender(template.format(args))

    @staticmethod
    def _make_template(level, template):
        return "["+level+"]"+template

    def _filter(self, level, template, args):
        if self._verbosity >= level:
            full_template = self._make_template(Logger.Levels[level], template)
            self._append(full_template, args)

    def debug(self, template, args=None):
        self._filter(Verbosity.Debug, template, args)

    def info(self, template, args=None):
        self._filter(Verbosity.Info, template, args)

    def warn(self, template, args=None):
        self._filter(Verbosity.Warn, template, args)

    def error(self, template, args=None):
        self._filter(Verbosity.Error, template, args)

    def fatal(self, template, args=None):
        self._filter(Verbosity.Fatal, template, args)


def _default_appender(msg):
    pass
