#!/usr/bin/env python
from xiblint import __version__
import argparse
import json
import os
import sys

from xiblint.config import Config
from xiblint.xibcontext import XibContext
import xiblint.rules


def make_epilog_text():
    description = "Lint rules:\n"

    for rule_name in sorted(xiblint.rules.rule_checkers.keys()):
        checker = xiblint.rules.rule_checkers[rule_name]
        description += "\t{}\n".format(rule_name)
        doc = sys.modules[checker.__module__].__doc__
        if doc is not None:
            for line in doc.strip().split("\n"):
                description += " " * 24 + "{}\n".format(line)

    return description


def main():
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
        config = Config()
    except IOError as ex:
        print('Error: {}\n'.format(ex))
        parser.print_usage()
        sys.exit(1)
    except ValueError as ex:
        print('Error: {}: {}\n'.format(ex, Config.filename, ex))
        parser.print_usage()
        sys.exit(1)

    #
    # Process paths
    #
    errors = []
    include_paths = args.paths or config.include_paths
    for path in include_paths:
        if os.path.isfile(path):
            checkers = config.checkers(path)
            errors += process_file(path, checkers)
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for filename in files:
                    if os.path.splitext(filename)[1].lower() in ('.storyboard', '.xib'):
                        file_path = os.path.join(root, filename)
                        checkers = config.checkers(file_path)
                        errors += process_file(file_path, checkers)
        else:
            print("Error: Invalid path '{}'".format(path))
            sys.exit(1)

    print_errors(errors, args.reporter)

    sys.exit(1 if errors else 0)


def process_file(file_path, checkers):
    context = XibContext(file_path)
    for rule_name, (checker, config) in checkers.items():
        context.rule_name = rule_name
        checker(config, context)
    return context.errors


def print_errors(errors, reporter):
    if reporter == "raw":
        for error_dict in errors:
            print("{}:{}: error: {} [rule: {}]".format(
                error_dict["file"],
                error_dict["line"],
                error_dict["error"],
                error_dict["rule"],
            ))
    elif reporter == "json":
        print(json.dumps(errors))


if __name__ == '__main__':
    main()
