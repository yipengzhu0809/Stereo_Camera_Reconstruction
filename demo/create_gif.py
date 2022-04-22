# -*-coding: utf-8 -*-

import os
import cv2
from core.utils import file_utils, image_utils


def load_data(load_dir, count):
    print("load image:{:0=4d}".format(count))
    frameL = cv2.imread(os.path.join(load_dir, "left_{:0=4d}.png".format(count)))
    frameR = cv2.imread(os.path.join(load_dir, "right_{:0=4d}.png".format(count)))
    dispL_colormap = cv2.imread(os.path.join(load_dir, "disparity_{:0=4d}.png".format(count)))
    depth_colormap = cv2.imread(os.path.join(load_dir, "depth_{:0=4d}.png".format(count)))
    return frameL, frameR, dispL_colormap, depth_colormap


def convert_images2gif(file_dir):
    image_list = file_utils.get_files_list(file_dir, prefix="left", postfix=None, basename=True)
    image_data = []
    for image_file in image_list:
        image_id = str(image_file).split("_")[1].split(".")[0]
        frameL, frameR, dispL, depth = load_data(file_dir, int(image_id))
        frame = image_utils.image_hstack([frameL, frameR])
        depth = image_utils.image_hstack([dispL, depth])
        vis = image_utils.image_vstack([frame, depth])
        image_data.append(vis)
        image_utils.cv_show_image("vis", vis, use_rgb=False,waitKey=5)
    image_utils.image_list2gif(image_data, image_size=[960,None], out_gif_path="../docs/test.gif", fps=2)


if __name__ == '__main__':
    image_dir = "../docs/gif"
    convert_images2gif(image_dir)
