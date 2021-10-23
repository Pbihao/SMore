# @Author: Pbihao
# @Time  : 23/10/2021 5:45 PM
import os
import sys
import argparse
import argcomplete
from clear_SMore_project import clear_SMore_project


def run():
    parser = argparse.ArgumentParser(description="Tools for SmartMore!")
    subparsers = parser.add_subparsers(help='commands')

    # clear_SMore_project
    parser_clean = subparsers.add_parser('clean', description="clean cache for SMore project directories",
                                         help="Clean cache for SMore project directories")
    parser_clean.add_argument("dir_list", type=str, nargs='*', default=[os.getcwd()],
                              help="list of directory path to clean, set None to clean local directory")
    parser_clean.set_defaults(func=clear_SMore_project)

    argcomplete.autocomplete(parser, always_complete_options=True)
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.parse_args(['-h'])
