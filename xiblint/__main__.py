#!/usr/bin/env python

import argparse
import json
import os
import sys

from xiblint import __version__


def make_epilog_text():
    import xiblint.rules
    description = "Lint rules:\n"

    for rule_name in sorted(xiblint.rules.rule_checkers.keys()):
        checker = xiblint.rules.rule_checkers[rule_name]
        description += "\t{}\n".format(rule_name)
        doc = checker.__doc__
        if doc is not None:
            for line in doc.strip().split("\n"):
                description += " " * 24 + "{}\n".format(line.strip())

    return description


def main():
    from .patch_element_tree import patch_element_tree
    patch_element_tree()

    parser = argparse.ArgumentParser(
        description='.xib / .storyboard linter',
        epilog=make_epilog_text(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-v", "--version", action="version",
                        version=__version__)
    parser.add_argument("--reporter", choices=("raw", "json"),
                        default="raw",
                        help="custom reporter to use")
    parser.add_argument("paths", nargs=argparse.REMAINDER,
                        help="lint only at the specified paths")
    args = parser.parse_args()

    try:
        from xiblint.config import Config
        config = Config()
    except IOError as ex:
        print('Error: {}\n'.format(ex))
        parser.print_usage()
        sys.exit(1)
    except ValueError as ex:
        print('Error: {}: {}\n'.format(Config.filename, ex))
        parser.print_usage()
        sys.exit(1)

    #
    # Process paths
    #
    errors = []
    include_paths = args.paths or config.include_paths
    for path in include_paths:
        if os.path.isfile(path):
            errors += process_file(path, config)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for filename in files:
                    if os.path.splitext(filename)[1].lower() in ('.storyboard', '.xib'):
                        file_path = os.path.join(root, filename)
                        errors += process_file(file_path, config)
        else:
            print("Error: Invalid path '{}'".format(path))
            sys.exit(1)

    print_errors(errors, args.reporter)

    sys.exit(1 if errors else 0)


def process_file(file_path, config):
    from xiblint.xibcontext import XibContext
    checkers = config.checkers(file_path)
    context = XibContext(file_path)
    if context.tree:
        for rule_name, klass in checkers.items():
            context.rule_name = rule_name
            rule_config = config.config_for_rule(file_path, rule_name)
            instance = klass(rule_config)
            instance.check(context)
    return context.errors


def print_errors(errors, reporter):
    if reporter == "raw":
        for error_dict in errors:
            error_str = error_dict['error']
            if 'rule' in error_dict:
                error_str += ' [rule: {}]'.format(error_dict['rule'])
            print("{}:{}: error: {}".format(
                error_dict["file"],
                error_dict["line"],
                error_str,
            ))
    elif reporter == "json":
        print(json.dumps(errors))


if __name__ == '__main__':
    main()
