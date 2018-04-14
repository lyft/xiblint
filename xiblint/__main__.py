#!/usr/bin/env python
from xiblint import __version__
import argparse
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
    parser.parse_args()

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
    success = True
    for path in config.include_paths:
        for root, _, files in os.walk(path):
            for file_path in [os.path.join(root, file) for file in files]:
                checkers = config.checkers(file_path)
                success = process_file(file_path, checkers) and success

    sys.exit(0 if success else 1)


def process_file(file_path, checkers):
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in [u".storyboard", u".xib"]:
        return True
    context = XibContext(file_path)
    for rule_name, checker in checkers.items():
        context.rule_name = rule_name
        checker(context)
    return context.success


if __name__ == '__main__':
    main()
