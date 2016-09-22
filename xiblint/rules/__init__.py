import inspect
from glob import glob
from os.path import basename, dirname
from importlib import import_module


def _collect_checkers():
    _rule_checkers = {}
    for file in glob(dirname(__file__) + "/*.py"):
        rule_name = basename(file)[:-3]
        module = import_module('xiblint.rules.' + rule_name)
        check = getattr(module, 'check', None)
        if inspect.isfunction(check):
            _rule_checkers[rule_name] = check
    return _rule_checkers

rule_checkers = _collect_checkers()
