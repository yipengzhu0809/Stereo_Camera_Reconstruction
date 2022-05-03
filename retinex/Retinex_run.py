import sys
import os

import cv2
import json

import Retinex_1

data_path = 'img'
img_list = os.listdir(data_path)
if len(img_list) == 0:
    print('Data directory is empty.')
    exit()

"""
with open('config.json', 'r') as f:
    config = json.load(f)
"""
config = {'sigma_list': [300,300,0.33], 'G': 5, 'b': 25, 'alpha': 125, 'beta': 46, 'low_clip':0.1, 'high_clip':0.6}

for img_name in img_list:
    if img_name == '.gitkeep':
        continue

    img = cv2.imread(os.path.join(data_path, img_name))

    print('msrcr processing......')
    img_msrcr = Retinex_1.MSRCR(
        img,
        config['sigma_list'],
        config['G'],
        config['b'],
        config['alpha'],
        config['beta'],
        config['low_clip'],
        config['high_clip']
    )
    cv2.imshow('MSRCR retinex', img_msrcr)
    cv2.imwrite("MSRCR_retinex.tif", img_msrcr)

    print('amsrcr processing......')
    img_amsrcr = Retinex_1.automatedMSRCR(
        img,
        config['sigma_list']
    )
    cv2.imshow('autoMSRCR retinex', img_amsrcr)
    cv2.imwrite('AutomatedMSRCR_retinex.tif', img_amsrcr)

    print('msrcp processing......')
    img_msrcp = Retinex_1.MSRCP(
        img,
        config['sigma_list'],
        config['low_clip'],
        config['high_clip']
    )

    shape = img.shape
    cv2.imshow('Image', img)

    cv2.imshow('MSRCP', img_msrcp)
    cv2.imwrite('MSRCP.tif', img_msrcp)
    cv2.waitKey()
