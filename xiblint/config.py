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
        with open(self.filename, 'r') as f:
            data = json.load(f)
        self.rules = data.get('rules', [])
        validate_rule_patterns(self.rules)
        default_rules_config = data.get('rules_config', {})
        self.include_paths = data.get('include_paths', [u'.'])
        self.paths = {
            abspath(path): PathConfig(self, default_rules_config, config)
            for (path, config) in data.get('paths', {}).items()
        }
        self.base_config = PathConfig(self, default_rules_config, {})

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

    def config_for_rule(self, file_path, rule_name):
        return self._config_for_file_path(file_path).config_for_rule(rule_name)


class PathConfig(object):
    def __init__(self, config, default_rules_config, data):
        self.config = config
        self.path_rules = data.get('rules')
        validate_rule_patterns(self.path_rules)
        self.excluded_rules = data.get('excluded_rules', [])
        validate_rule_patterns(self.excluded_rules)
        self._rules_config = (data.get('rules_config', {}) or
                              default_rules_config)

        # Filter checkers
        patterns = self.path_rules if self.path_rules is not None else self.config.rules
        excluded_patterns = self.excluded_rules
        self.checkers = {
            rule: klass for (rule, klass) in xiblint.rules.rule_checkers.items()
            if any(fnmatch(rule, pattern) for pattern in patterns) and
            not any(fnmatch(rule, pattern) for pattern in excluded_patterns)
        }

    def config_for_rule(self, rule_name):
        return self._rules_config.get(rule_name, {})
