"""
This module provides the base sparse command and a load hook for dynamically
adding other subcommands.  The "load_suparsers" function searches for modules
in the streamparse/bin directory that have a "subparser_hook" method. The
"subparser_hook" accepts a the sparse subparsers object and adds it's
subparser as needed.
"""

from __future__ import absolute_import

import argparse
import importlib
import os
import pkgutil
import sys


def load_suparsers(subparsers):
    """
    searches modules in streamparse/bin for a 'subparser_hook' method and calls
    the 'subparser_hook' method on the sparse subparsers object.
    """
    for _, mod_name, is_pkg in pkgutil.iter_modules([os.path.dirname(__file__)]):
        if not is_pkg and mod_name not in sys.modules:
            module = importlib.import_module('.{}'.format(mod_name),
                                             __package__)
            # check for the subparser hook
            if hasattr(module, 'subparser_hook'):
                module.subparser_hook(subparsers)


def main():
    """main entry point for sparse"""
    parser = argparse.ArgumentParser(prog='sparse',
                                     description='sparse: manage streamparse '
                                                 'clusters.',
                                     epilog='sparse provides a front-end to '
                                            'streamparse, a framework for '
                                            'creating Python projects for '
                                            'running, debugging, and '
                                            'submitting computation topologies '
                                            'against real-time streams, using '
                                            'Apache Storm. It requires java and'
                                            ' lein (Clojure build tool) to be '
                                            'on your $PATH, and uses lein and '
                                            'Clojure under the hood for JVM/'
                                            'Thrift interop.')
    subparsers = parser.add_subparsers()
    load_suparsers(subparsers)
    args = parser.parse_args()

    ### http://grokbase.com/t/python/python-bugs-list/12arsq9ayf/issue16308-undocumented-behaviour-change-in-argparse-from-3-2-3-to-3-3-0
    try:
        getattr(args, "func")
        args.func(args)
    # python3.3+ argparse changes
    except AttributeError:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
