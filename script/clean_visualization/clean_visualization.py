# @Author: Pbihao
# @Time  : 8/11/2021 11:04 AM
"""
This is a script to clean visualization file of SMore project
This script will remove directories [debug, result] under [~/result/test/{epoch}/]
If no arg is inputted, this script will clean local directory, in another word, '.'
This script will recursively search all subdirectories

******=>Be careful to use this script, all removed files can't be restored
"""

import sys
import os
import shutil
import tqdm


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


def clean_vis(root_path):
    dirs_path_to_clear = []

    if not os.path.exists(root_path):
        print(Colors.FAIL + "The path doesn't exist: " + Colors.ENDC)
        print("    {}".format(root_path))
        exit(0)

    for root, dirs, files in os.walk(root_path):
        if 'exp.yaml' not in files:
            continue

        test_path = os.path.join(root, "result", "test")
        if not os.path.exists(test_path):
            continue

        epochs = os.listdir(test_path)
        for epoch in epochs:
            debug_path = os.path.join(test_path, str(epoch), "debug")
            result_path = os.path.join(test_path, str(epoch), "result")
            if os.path.exists(debug_path):
                dirs_path_to_clear.append(debug_path)
            if os.path.exists(result_path):
                dirs_path_to_clear.append(result_path)

    if len(dirs_path_to_clear) == 0:
        print(Colors.OKGREEN + "No folders will be cleaned: " + Colors.ENDC)
        exit(0)

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
        for sub_dir_path in tqdm.tqdm(dirs_path_to_clear):
            if os.path.isdir(sub_dir_path):
                shutil.rmtree(sub_dir_path)
    except Exception as e:
        print('Failed to delete. Reason: %s' % e)
    print(Colors.OKGREEN + "All folders are cleaned!" + Colors.ENDC)


def clean_visualization(args):
    clean_vis(args.root_path)


if __name__ == "__main__":
    clean_vis("/home/pbihao/SMore/segmentation/exp/weida/paixian")