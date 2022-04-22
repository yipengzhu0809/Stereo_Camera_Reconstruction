#!/usr/bin/env bash

width=8
height=11
left_video=0
right_video=-1
save_dir="data/camera"
detect=True

python get_stereo_images.py \
    --left_video $left_video \
    --right_video $right_video \
    --width $width  \
    --height $height  \
    --save_dir $save_dir \
    --detect $detect \
