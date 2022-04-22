# -*- coding: utf-8 -*-

import numpy as np
import cv2
from core.utils.file_storage import load_stereo_coefficients


def get_rectify_transform(K1, D1, K2, D2, R, T, image_size):
    """
    获取用于畸变校正和立体校正的映射矩阵以及用于计算像素空间坐标的重投影矩阵
    cv2.stereoRectify()函数：
        (1)flags是标志位，CV_CALIB_ZERO_DISPARITY时，两幅校正后的图像的主点有相同的像素坐标。
           否则该函数会水平或垂直的移动图像，以使得其有用的范围最大
        (2)alpha是拉伸参数，如果设置为负或忽略，将不进行拉伸；
           如果设置为0，那么校正后图像只有有效的部分会被显示（没有黑色的部分）,
           如果设置为1，那么就会显示整个图像。设置为0~1之间的某个值，其效果也居于两者之间。
         R1-输出矩阵，第一个摄像机的校正变换矩阵（旋转变换）
         R2-输出矩阵，第二个摄像机的校正变换矩阵（旋转矩阵）
         P1-输出矩阵，第一个摄像机在新坐标系下的投影矩阵
         P2-输出矩阵，第二个摄像机在想坐标系下的投影矩阵
         Q -4*4的视差图到深度图的映射矩阵(disparity-to-depth mapping matrix )
    cv2.initUndistortRectifyMap()函数
        cameraMatrix-摄像机参数矩阵
        distCoeffs-畸变参数矩阵
        R- stereoCalibrate() 求得的R矩阵
        newCameraMatrix-矫正后的摄像机矩阵（可省略）
        Size-没有矫正图像的分辨率
        m1type-第一个输出映射的数据类型，可以为 CV_32FC1  或  CV_16SC2
        map1-输出的第一个映射变换
        map2-输出的第二个映射变换

    :param K1: Input/output camera intrinsic matrix for the first camera第一个相机的相机内参
    :param D1:  Input/output vector of distortion coefficients for the first camera 第一个相机的畸变系数
    :param K2: Input/output second camera intrinsic matrix for the second camera
    :param D2: Input/output vector of distortion coefficients for the second camera
    :param image_size:图像的大小(W,H)
    :param R: rotation matrix第一和第二个摄像机之间的旋转矩阵
    :param T: 第一和第二个摄像机之间的平移矩阵
    :param E: essential matrix本质矩阵
    :param F: fundamental matrix基本矩阵
    :return: stereoRectify的输出参数:
    :return:left_map_x
            left_map_y
            right_map_x
            right_map_y
            Q：4*4的视差图到深度图的映射矩阵(disparity-to-depth mapping matrix),即重投影矩阵Q
    """
    # R1, R2, P1, P2, Q, roi_left, roi_right = cv2.stereoRectify(K1, D1, K2, D2, image_size, R, T, alpha=0)
    R1, R2, P1, P2, Q, roi_left, roi_right = cv2.stereoRectify(K1, D1, K2, D2, image_size, R, T,
                                                               flags=cv2.CALIB_ZERO_DISPARITY, alpha=0.9)
    # Undistortion and Rectification(计算畸变矫正和立体校正的映射变换)
    # map_x: The first map of y values; map_y: The second map of y values
    left_map_x, left_map_y = cv2.initUndistortRectifyMap(K1, D1, R1, P1, image_size, cv2.CV_32FC1)
    right_map_x, right_map_y = cv2.initUndistortRectifyMap(K2, D2, R2, P2, image_size, cv2.CV_32FC1)
    return left_map_x, left_map_y, right_map_x, right_map_y, R1, R2, P1, P2, Q


def get_stereo_coefficients(stereo_file, rectify=True):
    """
    https://blog.csdn.net/Gordon_Wei/article/details/86319058
    重投影矩阵Q=[[1, 0, 0, -cx]
                 [0, 1, 0, -cy]
                 [0, 0, 0,  f]
                 [1, 0, -1/Tx, (cx-cx`)/Tx]]
    其中f为焦距，Tx相当于平移向量T的第一个参数
    :param stereo_file: 存储着双目标定的参数文件
    :param rectify:
    :return: 
    """
    # Get cams params
    K1, D1, K2, D2, R, T, E, F, R1, R2, P1, P2, Q, size = load_stereo_coefficients(stereo_file)
    config = {}
    config["size"] = size  # 图像分辨率
    config["K1"] = K1  # 左相机内参
    config["D1"] = D1  # 左相机畸变系数
    config["K2"] = K2  # 右相机内参
    config["D2"] = D2  # 右相机畸变系数
    config["R"] = R  # 旋转矩阵
    config["T"] = T  # 平移矩阵
    config["E"] = E  # essential matrix本质矩阵
    config["F"] = F  # fundamental matrix基本矩阵
    config["R1"] = R1
    config["R2"] = R2
    config["P1"] = P1
    config["P2"] = P2
    config["Q"] = Q
    if rectify:
        # 获取用于畸变校正和立体校正的映射矩阵以及用于计算像素空间坐标的重投影矩阵
        left_map_x, left_map_y, right_map_x, right_map_y, R1, R2, P1, P2, Q = get_rectify_transform(K1, D1, K2, D2,
                                                                                                    R, T, size)
        config["R1"] = R1
        config["R2"] = R2
        config["P1"] = P1
        config["P2"] = P2
        config["Q"] = Q
        config["left_map_x"] = left_map_x
        config["left_map_y"] = left_map_y
        config["right_map_x"] = right_map_x
        config["right_map_y"] = right_map_y
    focal_length = Q[2, 3]  # 相机焦距
    # baseline = T[0]  # 双目相机的基线长度，为平移向量T的第一个参数（取绝对值）单位：mm
    baseline = 1 / Q[3, 2]  # 基线也可以由Q[3, 2]=-1/Tx计算
    print("Q=\n{}\nfocal_length={}".format(Q, focal_length))
    print("T=\n{}\nbaseline    ={}mm".format(T, baseline))
    return config


# 双目相机参数
class stereoCamera(object):
    def __init__(self, width=640, height=480):
        # 左相机内参
        # self.cam_matrix_left = np.array([[1499.64168081943, 0, 1097.61651199043],
        #                                  [0., 1497.98941910377, 772.371510027325],
        #                                  [0., 0., 1.]])
        self.cam_matrix_left = np.asarray([[4.1929128272967574e+02, 0., 3.2356123553538390e+02],
                                           [0., 4.1931862286777556e+02, 2.1942548262685406e+02],
                                           [0., 0., 1.]])
        # 右相机内参
        # self.cam_matrix_right = np.array([[1494.85561041115, 0, 1067.32184876563],
        #                                   [0., 1491.89013795616, 777.983913223449],
        #                                   [0., 0., 1.]])
        self.cam_matrix_right = np.asarray([[4.1680693687859372e+02, 0., 3.2769747052057716e+02],
                                            [0., 4.1688284886037280e+02, 2.3285709632482832e+02],
                                            [0., 0., 1.]])

        # 左右相机畸变系数:[k1, k2, p1, p2, k3]
        # self.distortion_l = np.array([[-0.110331619900584, 0.0789239541458329, -0.000417147132750895,
        #                                0.00171210128855920, -0.00959533143245654]])
        self.distortion_l = np.asarray([[-2.9558582315073436e-02,
                                         1.5948145293240729e-01,
                                         -7.1046620767870137e-04,
                                         -6.5787270354389317e-04,
                                         -2.7169829618300961e-01]])
        # self.distortion_r = np.array([[-0.106539730103100, 0.0793246026401067, -0.000288067586478778,
        #                                -8.92638488356863e-06, -0.0161669384831612]])
        self.distortion_r = np.asarray([[-2.3391571805264716e-02,
                                         1.3648437316647929e-01,
                                         6.7233698457319337e-05,
                                         5.8610808515832777e-04,
                                         -2.3463198941301094e-01]])

        # 旋转矩阵
        # self.R = np.array([[0.993995723217419, 0.0165647819554691, 0.108157802419652],
        #                    [-0.0157381345263306, 0.999840084288358, -0.00849217121126161],
        #                    [-0.108281177252152, 0.00673897982027135, 0.994097466450785]])

        self.R = np.asarray([[9.9995518261153071e-01, 4.2888473189297411e-04, -9.4577389595457383e-03],
                             [-4.4122271031099070e-04, 9.9999905442083736e-01, -1.3024899043586808e-03],
                             [9.4571713984714298e-03, 1.3066044993798060e-03, 9.9995442630843034e-01]])

        # 平移矩阵
        # self.T = np.array([[-423.716923177417], [2.56178287450396], [21.9734621041330]])
        self.T = np.asarray([[-2.2987774547369614e-02], [3.0563972870288424e-05], [8.9781163185012418e-05]])

        R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(self.cam_matrix_left,
                                                          self.distortion_l,
                                                          self.cam_matrix_right,
                                                          self.distortion_r,
                                                          (width, height),
                                                          self.R,
                                                          self.T,
                                                          alpha=0)

        # 焦距
        # self.focal_length = 1602.46406  # 默认值，一般取立体校正后的重投影矩阵Q中的 Q[2,3]
        self.focal_length = Q[2, 3]  # 默认值，一般取立体校正后的重投影矩阵Q中的 Q[2,3]

        # 基线距离
        self.baseline = self.T[0]  # 单位：mm， 为平移向量的第一个参数（取绝对值）


if __name__ == "__main__":
    stereo_file = "../config/main_camera/stereo_cam.yml"
    config = get_stereo_coefficients(stereo_file, width=640, height=480)
