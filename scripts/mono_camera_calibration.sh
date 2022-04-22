#!/usr/bin/env bash

image_dir=data/lenacv-camera # 棋盘格图片
save_dir=configs/lenacv-camera # 保存标定结果
width=8
height=11
square_size=20 #mm
image_format=png # 图片格式，如png,jpg
show=True # 是否显示检测结果
# left camera calibration
python mono_camera_calibration.py \
    --image_dir  $image_dir \
    --image_format $image_format  \
    --square_size $square_size  \
    --width $width  \
    --height $height  \
    --prefix left  \
    --save_dir $save_dir \
    --show $show

# right camera calibration
python mono_camera_calibration.py \
    --image_dir  $image_dir \
    --image_format  $image_format  \
    --square_size $square_size  \
    --width $width  \
    --height $height  \
    --prefix right  \
    --save_dir $save_dir \
    --show $show
