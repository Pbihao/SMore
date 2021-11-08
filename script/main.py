# @Author: Pbihao
# @Time  : 23/10/2021 5:45 PM
import os
import sys
import argparse
import argcomplete
from clean_SMore_project.clean_SMore_project import clean_SMore_project
from copy_backbone.copy_backbone import copy_backbone
from clean_visualization.clean_visualization import clean_visualization


def run():
    parser = argparse.ArgumentParser(description="Tools for SmartMore!")
    subparsers = parser.add_subparsers(help='commands')

    # clean_SMore_project
    parser_clean = subparsers.add_parser('clean', description="clean cache for SMore project directories",
                                         help="Clean cache for SMore project directories")
    parser_clean.add_argument("dir_list", type=str, nargs='*', default=[os.getcwd()],
                              help="list of directory path to clean, set None to clean local directory")
    parser_clean.set_defaults(func=clean_SMore_project)

    # copy backbone
    parser_cp = subparsers.add_parser('cp', description="copy directory without cache and results",
                                      help="Copy SMore project backbone")
    parser_cp.add_argument("src_path", type=str,
                           help="path of directory path to be copied")
    parser_cp.add_argument("dst_path", type=str,
                           help="path of destination folder")
    parser_cp.set_defaults(func=copy_backbone)

    # clean visualization
    parser_clnvis = subparsers.add_parser('clnvis', description="remove directories [debug, result] under [~/result/test/{epoch}/]",
                                      help="Clean visualization files")
    parser_clnvis.add_argument("root_path", type=str, nargs='?', default=os.getcwd(),
                              help="This script will recursively search all subdirectories")
    parser_clnvis.set_defaults(func=clean_visualization)

    argcomplete.autocomplete(parser, always_complete_options=True)
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.parse_args(['-h'])
