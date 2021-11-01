#!/bin/python3
"""
This is a script to copy the directory of SMore project
This script will copy all files except under [model, output, progress, result]

Example to use ===>:
    python3 ./copy_backbone.py ./AP/ap_10_22  ./PET/pet_10_22'
    smt cp [src path] [dst path]
"""

import sys
import os
import shutil


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def copy_backbone_from_src_to_dst(src_path, dst_path):
    assert isinstance(src_path, str) and isinstance(dst_path, str)
    ignore_folder_names = ['model', 'output', 'progress', 'result']

    if 'exp.yaml' not in os.listdir(src_path):
        print(Colors.FAIL + "This is not a SMore folder: " + Colors.ENDC)
        print("    {}".format(dst_path))
        exit(0)

    if not os.path.isdir(src_path):
        print(Colors.FAIL + "This path is not a directory: " + Colors.ENDC)
        print("    {}".format(src_path))
        exit(0)

    if os.path.exists(dst_path):
        print(Colors.WARNING + "This path is already existing: " + Colors.ENDC)
        print("    {}".format(dst_path))
        while True:
            print(Colors.WARNING + "Please input y/n to overwrite/stop: " + Colors.ENDC, end='')
            opt = input().strip().lower()
            if opt == 'n' or opt == 'not':
                exit(0)
            if opt == 'y' or opt == "yes":
                try:
                    if os.path.isfile(dst_path) or os.path.islink(dst_path):
                        os.unlink(dst_path)
                    elif os.path.isdir(dst_path):
                        shutil.rmtree(dst_path)
                except Exception as e:
                    print('Failed to delete. Reason: %s' % e)
                break

    os.makedirs(dst_path)

    for item in os.listdir(src_path):
        item_path = os.path.join(src_path, item)
        if item in ignore_folder_names:
            os.makedirs(os.path.join(dst_path, item))
            continue

        try:
            if os.path.isfile(item_path):
                shutil.copy(item_path, dst_path)
            elif os.path.isdir(item_path):
                shutil.copytree(item_path, os.path.join(dst_path, item))
            else:
                print(Colors.FAIL + "Fail to copy!" + Colors.ENDC)
        except Exception as e:
            print('Failed to delete. Reason: %s' % e)

    print(Colors.OKGREEN + "All folders are copied!" + Colors.ENDC)


def copy_backbone(args):
    copy_backbone_from_src_to_dst(args.src_path, args.dst_path)
