import inspect
from glob import glob
from os.path import basename, dirname
from importlib import import_module


class Rule(object):
    def __init__(self, config):
        self.config = config

    def check(self, context):
        raise NotImplementedError()


def _class_name_for_file(filename):
    components = filename.split("_")
    return "".join(x.title() for x in components)


def _collect_checkers():
    _rule_checkers = {}
    for filepath in glob(dirname(__file__) + "/*.py"):
        rule_name = basename(filepath)[:-3]
        module = import_module('xiblint.rules.' + rule_name)
        class_name = _class_name_for_file(rule_name)
        klass = getattr(module, class_name, None)
        if inspect.isclass(klass):
            _rule_checkers[rule_name] = klass
    return _rule_checkers

rule_checkers = _collect_checkers()
