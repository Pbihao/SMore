# @Author: Pbihao
# @Time  : 27/10/2021 11:24 AM
import cv2
import numpy as np


def filter_component_by_area_size(mask, threshold):
    """
    This function will drop all components with size smaller than threshold
    :param threshold: [int, ... ] -> min size of component, "-1" means to ignore this category
    :param mask: [H, W] value of each pixel represents its category
    :return mask: [H, W] filtered mask
    """
    assert np.max(mask) < len(threshold)
    categories = np.unique(mask).astype(np.uint8)
    rectangles = []  # [[x, y, width, height, area, category], ... ]
    for category in categories:
        if threshold[category] == -1:
            continue
        components = (mask == category).astype(np.uint8)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(components, connectivity=8)
        """
        num_labels: int -> how many different components
        labels: [H, W] -> different components are represented by different id
        stats: [[x, y, width, height, area], ... ] -> min rectangle to cover
        centroids: [[x, y], ... ] -> center coordinate
        """
        target_labels = np.sort(np.unique(components * (labels + 1))[1:] - 1)  # labels start from 0, and background is also 0, so add 1 to  label to prevent from confusing with background
        for com_id in range(num_labels):
            if com_id not in target_labels:
                continue
            if stats[com_id][4] >= threshold[category]:
                rectangles.append([*stats[com_id], category])
            else:
                mask = mask * (labels != com_id)
    return mask, rectangles


if __name__ == "__main__":
    threshold = [-1, 2, 2, 3]
    mask = np.array([[0, 3, 3, 0],
                     [3, 0, 3, 1],
                     [0, 2, 3, 0],
                     [0, 0, 3, 2]])
    mask, rect = filter_component_by_area_size(mask, threshold)
    print(mask)
    print(rect)