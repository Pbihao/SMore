#!/bin/python3
"""
This is a script to clean directories of SMore machine learning project
This script will clean all files under [model, output, progress, result]
If no arg is inputted, this script will clean local directory, in another word, '.'

Example to use ===>:
    python3 ./clean_SMore_project.py ./AP/ap_10_22  ./PET/pet_10_22
or
    chmod +x ./clean_SMore_project.py
    ./clean_SMore_project.py ./AP/ap_10_22

******=>Be careful to use this script, all removed files can't be restored
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


def clean_project(dir_paths):
    dirs_path_to_clear = set()
    clear_folder_names = ['model', 'output', 'progress', 'result']
    for dir_path in dir_paths:
        if not os.path.exists(dir_path):
            print(Colors.FAIL + "This path doesn't exist: " + Colors.ENDC)
            print("    {}".format(dir_path))
            exit(0)
        dir_path = os.path.abspath(dir_path)

        sub_dirs = os.listdir(dir_path)

        if 'exp.yaml' not in sub_dirs:
            print(Colors.FAIL + "This is not a SMore structure folder: " + Colors.ENDC)
            print("    {}".format(dir_path))
            exit(0)

        for sub_dir_name in sub_dirs:
            if sub_dir_name not in clear_folder_names:
                continue
            sub_dir_path = os.path.join(dir_path, sub_dir_name)
            dirs_path_to_clear.add(sub_dir_path)

    print(Colors.WARNING + "These folders will be cleaned: " + Colors.ENDC)
    for path in dirs_path_to_clear:
        print("    {}".format(path))

    while True:
        print(Colors.WARNING + "Please input y/n to start/stop clean script: " + Colors.ENDC, end='')
        opt = input().strip().lower()
        if opt == 'n' or opt == 'not':
            quit()
        if opt == 'y' or opt == "yes":
            break

    try:
        for sub_dir_path in dirs_path_to_clear:
            for name in os.listdir(sub_dir_path):
                rm_path = os.path.join(sub_dir_path, name)
                if os.path.isfile(rm_path) or os.path.islink(rm_path):
                    os.unlink(rm_path)
                elif os.path.isdir(rm_path):
                    shutil.rmtree(rm_path)
    except Exception as e:
        print('Failed to delete. Reason: %s' % e)
    print(Colors.OKGREEN + "All folders are cleaned!" + Colors.ENDC)


def clean_SMore_project(args):
    clean_project(args.dir_list)
