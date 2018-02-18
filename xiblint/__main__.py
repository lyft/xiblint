#!/usr/bin/env python
from xiblint import __version__
import argparse
import os
import sys
import json

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
                        help="custom reporter to use (optional)")
    args = parser.parse_args()
    reporter = args.reporter

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
    for root, _, files in os.walk(u'.'):
        for file_path in [os.path.join(root, file) for file in files]:
            checkers = config.checkers(file_path)
            errors = errors + process_file(file_path, checkers, reporter)

    print_errors(errors, reporter)

    sys.exit(0 if errors.count == 0 else 1)


def process_file(file_path, checkers, reporter):
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in [u".storyboard", u".xib"]:
        return []
    context = XibContext(file_path)
    for rule_name, checker in checkers.items():
        context.rule_name = rule_name
        checker(context)
    return context.errors


def print_errors(errors, reporter):
    if reporter == "raw":
        for error_dict in errors:
            print("{}:{}: error: {} [rule: {}]".format(
                error_dict["file"],
                error_dict["line"],
                error_dict["error"],
                error_dict["rule"]
            ))
    elif reporter == "json":
        print(json.dumps(errors))


if __name__ == '__main__':
    main()
