# -*-coding: utf-8 -*-

import cv2
import numpy as np


def StereoSGBM_create(minDisparity=None, numDisparities=None, blockSize=None, P1=None, P2=None,
                      disp12MaxDiff=None, preFilterCap=None, uniquenessRatio=None,
                      speckleWindowSize=None, speckleRange=None, mode=None):
    """
    创建左右视差图
    :param minDisparity:最小视差值。通常我们期望这里是0，但当校正算法移动图像时，有时需要设置。
    :param numDisparities: 最大视差值，必须大于0，定义视差边界。
    :param blockSize: 匹配块的块大小。推荐使用[3-11]，推荐使用奇数，因为奇数大小的块有一个中心。
    :param P1:
    :param P2:  负责平滑图像，规则是P2>P1
    :param disp12MaxDiff: 视差计算的最大像素差
    :param preFilterCap: 过滤前使用的值,在块匹配之前，计算图像x轴的一个导数，并用于检查边界[-prefiltercap, prefiltercap]
                         其余的值用Birchfield-Tomasi代价函数处理
    :param uniquenessRatio: 经过成本函数计算，此值用于比较。建议取值范围[5-15]
    :param speckleWindowSize: 过滤删除大的值，得到一个更平滑的图像。建议取值范围[50-200]
    :param speckleRange: 使用领域检查视差得到一个平滑的图像。如果你决定尝试，我建议1或2
                         这个值会乘以16！OpenCV会这样做，所以你不需要自己去乘
    :param mode:
    :return:
    """


def reprojectImageTo3D(disparity, Q, _3dImage=None, handleMissingValues=None, ddepth=None):
    """
    :param disparity: 输入视差图
    :param Q: 输入4*4的视差图到深度图的映射矩阵，即重投影矩阵 通过stereoRectify得到
            (disparity-to-depth mapping matrix)
    :param _3dImage: 映射后存储三维坐标的图像
             contains 3D coordinates of the point (x,y) computed from the disparity map
    :param handleMissingValues: 计算得到的非正常值是否给值，如果为true则给值10000
    :param ddepth: 输出类型 -1 即默认为CV_32FC3 还可以是 CV_16S, CV_32S, CV_32F
    :return:
    """
    return cv2.reprojectImageTo3D(disparity, Q, _3dImage, handleMissingValues, ddepth)


def get_depth(disparity, Q, scale=1.0, method=True):
    """
    运算过程：https://blog.csdn.net/Gordon_Wei/article/details/86319058
    reprojectImageTo3D(disparity, Q),输入的Q,单位必须是毫米(mm)
    :param disparity: 视差图
    :param Q: 重投影矩阵Q=[[1, 0, 0, -cx]
                           [0, 1, 0, -cy]
                           [0, 0, 0,  f]
                           [1, 0, -1/Tx, (cx-cx`)/Tx]]
            其中f为焦距，Tx相当于平移向量T的第一个参数
    :param scale: 单位变换尺度,默认scale=1.0,单位为毫米
    :return depth:ndarray(np.uint16),depth返回深度图, 即距离
    """
    # 将图片扩展至3d空间中，其z方向的值则为当前的距离
    if method:
        points_3d = cv2.reprojectImageTo3D(disparity, Q)  # 单位是毫米(mm)
        x, y, depth = cv2.split(points_3d)
    else:
        # baseline = abs(camera_config["T"][0])
        baseline = 1 / Q[3, 2]  # 基线也可以由T[0]计算
        fx = abs(Q[2, 3])
        depth = (fx * baseline) / disparity
    depth = depth * scale
    # depth = np.asarray(depth, dtype=np.uint16)
    depth = np.asarray(depth, dtype=np.float32)
    return depth


class WLSFilter():
    def __init__(self, left_matcher, lmbda=80000, sigma=1.3):
        # WLS滤波平滑优化图像
        self.filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
        self.filter.setLambda(lmbda)
        self.filter.setSigmaColor(sigma)

    def disparity_filter(self, dispL, imgL, dispR):
        filter_displ = self.filter.filter(dispL, imgL, None, dispR)
        return filter_displ


def get_filter_disparity(imgL, imgR, use_wls=True, sgbm="param1"):
    """
    进行立体匹配，计算视差图
    https://github.com/aliyasineser/stereoDepth/blob/master/stereo_depth.py
    :param imgL: 畸变校正和立体校正后的左视图
    :param imgR：畸变校正和立体校正后的右视图
    :param use_wls：是否使用WLS滤波器对视差图进行滤波
    :param sgbm：立体匹配方法SGBM的参数类型
    :return dispL:ndarray(np.float32),返回视差图
    """
    channels = 1 if imgL.ndim == 2 else 3
    blockSize = 3
    if sgbm == "param1":
        paramL = {"minDisparity": 0,
                  "numDisparities": 5 * 16,
                  "blockSize": blockSize,
                  "P1": 8 * 3 * blockSize,
                  "P2": 32 * 3 * blockSize,
                  "disp12MaxDiff": 12,
                  "uniquenessRatio": 10,
                  "speckleWindowSize": 50,
                  "speckleRange": 32,
                  "preFilterCap": 63,
                  "mode": cv2.STEREO_SGBM_MODE_SGBM_3WAY
                  }
    elif sgbm == "param2":
        paramL = {"minDisparity": 0,
                  "numDisparities": 5 * 16,
                  "blockSize": blockSize,
                  "P1": 8 * 3 * blockSize,
                  "P2": 32 * 3 * blockSize,
                  "disp12MaxDiff": 12,
                  "uniquenessRatio": 10,
                  "speckleWindowSize": 50,
                  "speckleRange": 32,
                  "preFilterCap": 63,
                  "mode": cv2.STEREO_SGBM_MODE_SGBM_3WAY
                  }
    else:
        paramL = {'minDisparity': 0,
                  'numDisparities': 128,
                  'blockSize': blockSize,
                  'P1': 8 * channels * blockSize ** 2,
                  'P2': 32 * channels * blockSize ** 2,
                  'disp12MaxDiff': 1,
                  'preFilterCap': 63,
                  'uniquenessRatio': 15,
                  'speckleWindowSize': 100,
                  'speckleRange': 1,
                  'mode': cv2.STEREO_SGBM_MODE_SGBM_3WAY
                  }

    matcherL = cv2.StereoSGBM_create(**paramL)
    # 计算视差图
    dispL = matcherL.compute(imgL, imgR)
    dispL = np.int16(dispL)
    # WLS滤波平滑优化图像
    use_wls=1
    if use_wls:
        # paramR = paramL
        # paramR['minDisparity'] = -paramL['numDisparities']
        # matcherR = cv2.StereoSGBM_create(**paramR)
        matcherR = cv2.ximgproc.createRightMatcher(matcherL)
        dispR = matcherR.compute(imgR, imgL)
        dispR = np.int16(dispR)
        lmbda = 80000
        sigma = 1.3
        filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=matcherL)
        filter.setLambda(lmbda)
        filter.setSigmaColor(sigma)
        dispL = filter.filter(dispL, imgL, None, dispR)
        dispL = np.int16(dispL)
    # 除以16得到真实视差（因为SGBM算法得到的视差是×16的）
    dispL[dispL < 0] = 0
    dispL = dispL.astype(np.float32) / 16.
    return dispL


def get_simple_disparity(imgL, imgR):
    """
    http://www.manongjc.com/detail/13-etrvdspcpszsbcs.html
    :param imgL: 畸变校正和立体校正后的左视图
    :param imgR：畸变校正和立体校正后的右视图
    :return dispL:ndarray(np.float32),返回视差图
    """
    # SGBM参数设置
    blockSize = 8
    channels = 3
    matcherL = cv2.StereoSGBM_create(minDisparity=1,
                                     numDisparities=64,
                                     blockSize=blockSize,
                                     P1=8 * channels * blockSize,
                                     P2=32 * channels * blockSize,
                                     disp12MaxDiff=-1,
                                     preFilterCap=1,
                                     uniquenessRatio=10,
                                     speckleWindowSize=100,
                                     speckleRange=100,
                                     mode=cv2.STEREO_SGBM_MODE_HH)
    # 计算视差图
    dispL = matcherL.compute(imgL, imgR)
    dispL = np.int16(dispL)
    # SGBM得到的CV_16S格式的disparity矩阵，需除以16得到真实视差图
    dispL[dispL < 0] = 0
    dispL = np.divide(dispL.astype(np.float32), 16.)
    return dispL


def get_visual_depth(depth, clip_max=6000):
    """
    将输入深度图转换为伪彩色图，方面可视化
    :param depth: ndarray,depth深度图, 即距离
    :param clip_max:
    :return:
    """
    depth = np.clip(depth, 0, clip_max)
    # 归一化到0-255
    depth = cv2.normalize(src=depth, dst=depth, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX)
    depth = np.uint8(depth)
    depth_colormap = cv2.applyColorMap(depth, cv2.COLORMAP_JET)
    return depth_colormap


def get_visual_disparity(disp, clip_max=6000):
    """
    将输入视差图转换为uint8类型，方面可视化
    :param disp: ndarray 视差图
    :param clip_max:
    :return:
    """
    disp = np.clip(disp, 0, clip_max)
    disp = np.uint8(disp)
    return disp
