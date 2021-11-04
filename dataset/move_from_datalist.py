import os
import shutil
import tqdm


def convert_path(path, prefix=None):
    """
    path: str
    prefix: bool -> set None to transpose, 
    "/data/home/bohaopeng..." -> "/home/bohaopeng"
    or
    "/home/bohaopeng"         -> "/data/home/bohaopeng..."
    """
    already_has_prefix = path[:5] == "/data"
    if already_has_prefix and (prefix is None or not prefix):
        path = path[5:]
    elif not already_has_prefix and (prefix is None or prefix):
        path = "/data" + path
    return path



def merge_datalist(file_path):
    """
    :param file_path: str -> path to list of datalist
    :return datalist: [path, ... ] -> merged datalist
    """
    datalist = []
    with open(file_path, 'r') as f:
        paths = f.readlines()
        for datalist_path in paths:
            datalist_path = datalist_path.strip()
            datalist_path = convert_path(datalist_path, prefix=True)
            if not os.path.isfile(datalist_path):
                print("This datalist path doesn't exist:", datalist_path)
                continue
            with open(datalist_path, 'r') as fr:
                sub_lit = fr.readlines()
            sub_lit = list(filter(lambda path: path != '', map(lambda path: path.strip(), sub_lit)))
            datalist += sub_lit
    datalist = list(set(datalist))
    datalist.sort()
    return datalist


def copy_from_datalist(data_dir_path, ori_datalist_path, new_datalist_path):
    """
    :param data_dir_path:  str -> path of directory to store images and annotates
    :param ori_datalist_path: str -> path of original datalist file
    :param new_datalist_path: str -> path of new datalist file

    Example:
    copy_from_datalist("/data/home/bohaopeng/SMore/dataset/weida/paixian/1103/data", 
                       "/data/home/bohaopeng/SMore/dataset/weida/paixian/1103/ori_train.txt", 
                       "/data/home/bohaopeng/SMore/dataset/weida/paixian/1103/datalist/train.txt")
    copy images and annotates in ori_datalist_path file, put them under data_dir_path
    and generate new datalist file in new_datalist_path
    """
    with open(ori_datalist_path, 'r') as f:
        datalist = f.readlines()

    new_dir_path = os.path.split(new_datalist_path)[0]
    if not os.path.exists(new_dir_path):
        os.makedirs(new_dir_path)
    if not os.path.exists(data_dir_path):
        os.makedirs(data_dir_path)

    new_datalist = open(new_datalist_path, "w")

    for data in tqdm.tqdm(datalist):
        data = data.strip()
        img_path = convert_path(data.split(',')[0], prefix=True)
        json_path = convert_path(data.split(',')[1], prefix=True)
        
        new_img_path = os.path.join(data_dir_path, os.path.split(img_path)[1])
        new_json_path = os.path.join(data_dir_path, os.path.split(json_path)[1])

        new_datalist.write("{},{}\n".format(new_img_path[5:], new_json_path[5:]))
        shutil.copy(img_path, new_img_path)

        if os.path.exists(json_path):
            shutil.copy(json_path, new_json_path)

    new_datalist.close()

if __name__ == "__main__":
    data = merge_datalist("/data/home/bohaopeng/SMore/dataset/weida/paixian/1103/train_datalist.txt")
    data = list(map(lambda x: x + '\n', data))
    with open("/data/home/bohaopeng/SMore/dataset/weida/paixian/1103/ori_train.txt", 'w') as f:
        f.writelines(data)
    copy_from_datalist("/data/home/bohaopeng/SMore/dataset/weida/paixian/1103/data", 
                       "/data/home/bohaopeng/SMore/dataset/weida/paixian/1103/ori_train.txt", 
                       "/data/home/bohaopeng/SMore/dataset/weida/paixian/1103/datalist/train.txt")
