# @Author: Pbihao
# @Time  : 25/10/2021 8:07 PM
import cv2
import random
import numpy as np


def color_mask(mask):
    """
    :param mask: [H, W], value of each pixcel indicates the category
    :return image: [H, W, 3] different categories will be indicated different color
    """
    colors = [[0, 0, 0], [0, 0, 255], [0, 255, 0], [255, 0, 0],
              [0, 255, 255], [255, 0, 255], [255, 255, 0], [255, 255, 255]]
    category_list = np.unique(mask)
    category_list.sort()
    category_num = len(category_list)
    assert category_num <= 8 and np.max(category_list) < 8
    assert len(mask.shape) == 2
    res = np.zeros((*mask.shape, 3))
    for category in category_list:
        res[mask == category] = colors[category]
    return res


if __name__ == "__main__":
    mask = np.zeros((20, 20))
    mask[10, 10] = 1
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    from matplotlib import pyplot as plt
    plt.imshow(mask)
    plt.show()
