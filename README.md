# Camera-Calibration-Reconstruct

本项目实现双目相机的`双目标定`，`立体校正（含消除畸变)`，`立体匹配`，`视差计算`和`深度计算/3D坐标计算`

- [x] 支持双USB连接线的双目摄像头
- [x] 支持单USB连接线的双目摄像头(左右摄像头被拼接在同一个视频中显示)
- [x] 支持单目相机标定:[mono_camera_calibration.py](mono_camera_calibration.py)
- [x] 支持双目相机标定:[stereo_camera_calibration.py](stereo_camera_calibration.py)
- [x] 支持使用WLS滤波器对视差图进行滤波
- [x] 支持双目测距(鼠标点击图像即可获得其深度距离)
- [x] 支持Open3D和PCL点云显示

## 1.目录结构

```
.
├── config       # 相机参数文件
├── core         # 相机核心算法包
├── data         # 相机采集的数据
├── demo         # demo文件
├── libs         # 第三方依赖包
├── scripts       # 脚本
│   ├── mono_camera_calibration.sh     # 单目相机校准脚本
│   └── stereo_camera_calibration.sh   # 双目相机校准脚本
├── get_stereo_images.py                  # 采集标定文件
├── mono_camera_calibration.py            # 单目相机标定
├── stereo_camera_calibration.py          # 双目相机标定
├── requirements.txt                      # 依赖包
└── README.md

```

# 2. Environment

- 依赖包，可参考[requirements.txt](requirements.txt)
- python-pcl (安装python-pcl需要一丢丢耐心，是在不行，就用open3d吧)
- open3d-python=0.7.0.0
- opencv-python
- opencv-contrib-python

## 3.双目相机标定和校准

#### (1) 采集标定板的左右视图

```bash
bash scripts/get_stereo_images.sh
```

- 采集数据前，请调节相机焦距，尽可能保证视图中标定板清洗可见
- 采集棋盘格图像时，标定板一般占视图1/2到1/3左右
- 建议设置`detect=True`，这样可实时检测棋盘格
- 按键盘`s`或者`c`保存左右视图图片

|left_image                        |right_image                           |
|:--------------------------------:|:------------------------------------:|
|![Image text](docs/left_chess.png)|![Image text](docs/right_chess.png)   |

#### (2) [单目相机校准](scripts/mono_camera_calibration.sh)

- `bash scripts/mono_camera_calibration.sh`
- 若误差超过0.1，建议重新调整摄像头并标定

```bash
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
```

执行后，在`$save_dir`目录下会生成`left_cam.yml`和`right_cam.yml`左右相机参数文件

#### (3) [双目相机校准](scripts/stereo_camera_calibration.sh)
- `bash scripts/stereo_camera_calibration.sh`
- 若误差超过0.1，建议重新调整摄像头并标定

```bash
image_dir=data/lenacv-camera # 棋盘格图片
save_dir=configs/lenacv-camera # 保存标定结果
width=8
height=11
square_size=20 #mm
image_format=png # 图片格式，如png,jpg
#show=True # 是否显示检测结果
show=False # 是否显示检测结果
# stereo camera calibration
python stereo_camera_calibration.py \
    --left_file $save_dir/left_cam.yml \
    --right_file $save_dir/right_cam.yml \
    --left_prefix left \
    --right_prefix right \
    --width $width \
    --height $height \
    --left_dir $image_dir \
    --right_dir $image_dir \
    --image_format  $image_format  \
    --square_size $square_size \
    --save_dir $save_dir 
```

执行后，在`$save_dir`目录下会生成`stereo_cam.yml`相机参数文件

## 4.视差图和深度图

- 运行Demo计算视差图并恢复深度图

|      参数           |类型    |说明    |
|:-------------------:|:------:|:------|
| stereo_file    | str    | 双目相机的配置文件，如"configs/lenacv-camera/stereo_cam.yml"    |
| left_video          | str    | 左路相机ID或者视频文件    |
| right_video         | str    | 右路相机ID或者视频文件    |
| left_file           | str    | 左路测试图像文件    |
| right_file          | str    | 右路测试图像文件    |
| filter              | bool   | 是否对视差图进行滤波    |

```bash
python demo.py  \
  --stereo_file "configs/lenacv-camera/stereo_cam.yml" \
  --left_video "data/lenacv-video/left_video.avi" \
  --right_video "data/lenacv-video/right_video.avi" \
  --filter True
```
- 对视差图进行滤波，效果会好很多 

|      左视图                                       |右视图                                                  |
|:-------------------------------------------------:|:------------------------------------------------------:|
| ![Image text](docs/left.png)                      | ![Image text](docs/right.png)                          |
|      **视差图(未滤波)**                           |**深度图(未滤波)**                                                  |
| ![Image text](docs/disparity.png)                 | ![Image text](docs/depth.png)                      |
|      **视差图(滤波后)**                             |**深度图(滤波后)**                                                  |
| ![Image text](docs/disparity_filter.png)          | ![Image text](docs/depth_filter.png)                      |

- 效果图

![Image text](docs/demo.gif) 

## 5.双目测距

- 运行`demo.py`后，鼠标点击图像任意区域，终端会打印对应距离
- 鼠标点击手部区域会打印距离摄像头的距离约633mm,即0.63米，还是比较准的
```
(x,y)=(203,273),depth=633.881653mm
(x,y)=(197,329),depth=640.386047mm
(x,y)=(222,292),depth=631.549072mm
(x,y)=(237,270),depth=630.389221mm
(x,y)=(208,246),depth=652.560669mm
```

## 6.3D点云

- 3D点云显示，使用open3d
- 可以用鼠标旋转坐标轴，放大点云

 ![Image text](docs/3d-points.png) 
  
## 7.参考资料

- https://github.com/aliyasineser/stereoDepth
- <真实场景的双目立体匹配（Stereo Matching）获取深度图详解> : https://www.cnblogs.com/riddick/p/8486223.html
- <双目测距理论及其python实现> https://blog.csdn.net/dulingwen/article/details/98071584
- <Ubuntu 18.04安装python-pcl> https://blog.csdn.net/weixin_47047999/article/details/119088321 (亲测可用)


