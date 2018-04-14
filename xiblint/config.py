import json
from os.path import abspath
from fnmatch import fnmatch

import xiblint.rules


def validate_rule_patterns(patterns):
    for pattern in (patterns or []):
        if not any(fnmatch(key, pattern) for key in xiblint.rules.rule_checkers):
            print("Warning: Rule pattern '{}' matches no rules".format(pattern))


class Config(object):
    filename = '.xiblint.json'

    def __init__(self):
        with open(self.filename, 'r') as file:
            data = json.load(file)
        self.rules = data.get('rules', [])
        validate_rule_patterns(self.rules)
        self.include_paths = data.get('include_paths', [u'.'])
        self.paths = {abspath(path): PathConfig(self, config)
                      for (path, config) in data.get('paths', {}).items()}
        self.base_config = PathConfig(self, {})

    def _config_for_file_path(self, file_path):
        file_path = abspath(file_path)
        for path, config in self.paths.items():
            if file_path == path:
                return config
            if file_path.startswith(path + '/'):
                return config
        return self.base_config

    def checkers(self, file_path):
        return self._config_for_file_path(file_path).checkers


class PathConfig(object):
    def __init__(self, config, data):
        self.config = config
        self.path_rules = data.get('rules')
        validate_rule_patterns(self.path_rules)
        self.excluded_rules = data.get('excluded_rules', [])
        validate_rule_patterns(self.excluded_rules)

        # Filter checkers
        patterns = self.path_rules if self.path_rules is not None else self.config.rules
        excluded_patterns = self.excluded_rules
        self.checkers = {
            rule: checker for (rule, checker) in xiblint.rules.rule_checkers.items()
            if any(fnmatch(rule, pattern) for pattern in patterns) and
            not any(fnmatch(rule, pattern) for pattern in excluded_patterns)
        }
