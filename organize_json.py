# @Author: Pbihao
# @Time  : 21/10/2021 5:24 PM
import os
import shutil
import json
import tqdm


def get_all_labels(rt_path='.'):
    """
    search all labels of json files under rt_path dir
    :param rt_path: str
    :return: [label1, label2]
    """
    all_labels = []
    for rt, d, files in os.walk(rt_path):
        for file in files:
            if os.path.splitext(file)[1] != '.json':
                continue

            anno_path = os.path.join(rt, file)
            with open(anno_path) as f:
                anno = json.load(f)
            for shape in anno['shapes']:
                lab = shape['label']
                if lab not in all_labels:
                    all_labels.append(lab)
    return all_labels


def search_labeled_data(labels, dst_path, rt_path='.', debug=False):
    """
    search all json and image files under rt_path including given labels, then copy them to the given dst_path
    :param labels: [label1, label2, ...] or str  json file including these labels will be searched
    :param rt_path: str  search all files under this directory
    :param dst_path: str  copy files to this path
    :param debug: set True to print all new paths
    """
    print("===> Start to search: {}".format(os.path.abspath(rt_path)))
    for rt, d, files in tqdm.tqdm(os.walk(rt_path)):
        if os.path.abspath(rt) == os.path.abspath(dst_path):
            continue
        for file in files:
            if os.path.splitext(file)[1] != '.json':
                continue
            if debug:
                print(file)
            anno_path = os.path.join(rt, file)
            with open(anno_path) as f:
                anno = json.load(f)
            contained = False
            for shape in anno['shapes']:
                lab = shape['label']
                if lab in labels:
                    contained = True
                    break
            if not contained:
                continue
            img_path = os.path.join(rt, anno['imagePath'])
            assert os.path.exists(img_path)

            if not os.path.exists(dst_path):
                os.makedirs(dst_path)

            new_anno_path = os.path.join(dst_path, file)
            new_img_path = os.path.join(dst_path, anno['imagePath'])

            shutil.copy(img_path, new_img_path)
            shutil.copy(anno_path, new_anno_path)

            if debug:
                print("New img path: {}".format(new_img_path))
                print("New anno path: {}".format(new_anno_path))


def generate_datalist_from_dir(dir_path, dst_file_path, delimiter=',', prefix=None):
    """
    generate datalist in the directory of dir_path
    :param dir_path: path to json and image files -> str of dir
    :param dst_file_path: path to save datalist file -> str of file
    :param delimiter: delimiter to delimit image path and json path -> str
    :param prefix: use prefix to replace original dir_path
    """
    assert not os.path.exists(dst_file_path) or os.path.isfile(dst_file_path)
    if not os.path.exists(os.path.split(dst_file_path)[0]):
        os.makedirs(os.path.split(dst_file_path)[0])
    datalist = open(dst_file_path, "w")
    file_names = os.listdir(dir_path)
    for file_name in file_names:
        if os.path.splitext(file_name)[1] != '.json':
            continue
        anno_path = os.path.join(dir_path, file_name)
        with open(anno_path) as f:
            anno = json.load(f)
        img_path = os.path.join(dir_path, anno['imagePath'])

        if prefix is None:
            img_path = os.path.abspath(img_path)
            anno_path = os.path.abspath(anno_path)
        else:
            img_path = os.path.join(prefix, anno['imagePath'])
            anno_path = os.path.join(prefix, file_name)
        line = img_path + delimiter + anno_path + '\n'
        datalist.write(line)
    datalist.close()


if __name__ == "__main__":
    AP_labels = ['线圈划伤', 'AP划伤', 'AP划伤_ignore', '线圈划伤_ignore']
    paixian_labels = ['排线破损']
    PET_labels = ['PET破损', 'PET褶皱', 'PET褶皱_Nostsure', 'PET破损_Notsure', 'zhezhou_ignore']
    boli_labels = ['玻璃异色', '玻璃破损', '玻璃划伤', '玻璃划伤_ignore', '玻璃碰伤']

    # search_labeled_data(PET_labels, dst_path='./PET/data')
    # search_labeled_data(PET_labels, dst_path='./PET/data')
    # search_labeled_data(AP_labels, dst_path='./AP/data')
    # search_labeled_data(boli_labels, dst_path='./boli/data')

    generate_datalist_from_dir('./AP/data', './AP/datalist/train.txt', prefix='/home/bohaopeng/SMore/dataset/weida/AP/data')
    generate_datalist_from_dir('./boli/data', './boli/datalist/train.txt', prefix='/home/bohaopeng/SMore/dataset/weida/boli/data')
    generate_datalist_from_dir('./paixian/data', './paixian/datalist/train.txt', prefix='/home/bohaopeng/SMore/dataset/weida/paixian/data')


