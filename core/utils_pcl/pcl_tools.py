# -*-coding: utf-8 -*-

import pcl
import pcl.pcl_visualization
import numpy as np


class PCLCloudViewer(object):
    def __init__(self, point_cloud=None):
        self.point_cloud = point_cloud
        self.cloud = pcl.PointCloud_PointXYZRGBA()
        self.viewer = pcl.pcl_visualization.CloudViewing()

    def add_3dpoints(self, points_3d, image):
        """
        :param points_3d: 像素点的3D坐标(X,Y,Z)
        :param image:
        :return:
        """
        self.point_cloud = DepthColor2PointXYZRGBA(points_3d, image)

    def show(self):
        self.cloud.from_array(self.point_cloud)
        self.viewer.ShowColorACloud(self.cloud)
        v = not (self.viewer.WasStopped())
        return v


def DepthColor2PointXYZRGBA(points_3d, image):
    """深度、颜色转换为点云"""
    height, width = points_3d.shape[0:2]
    size = height * width
    points_ = points_3d.reshape(height * width, 3)
    colors_ = image.reshape(height * width, 3).astype(np.int64)
    # 颜色信息
    blue = colors_[:, 0].reshape(size, 1)
    green = colors_[:, 1].reshape(size, 1)
    red = colors_[:, 2].reshape(size, 1)
    rgb = np.left_shift(blue, 0) + np.left_shift(green, 8) + np.left_shift(red, 16)
    # 将坐标+颜色叠加为点云数组
    pointcloud = np.hstack((points_, rgb)).astype(np.float32)

    # 删掉一些不合适的点
    X = pointcloud[:, 0]
    Y = pointcloud[:, 1]
    Z = pointcloud[:, 2]

    # 下面参数是经验性取值，需要根据实际情况调整
    idx1 = np.where(Z <= 0)
    idx2 = np.where(Z > 15000)
    idx3 = np.where(X > 10000)
    idx4 = np.where(X < -10000)
    idx5 = np.where(Y > 10000)
    idx6 = np.where(Y < -10000)
    idx = np.hstack((idx1[0], idx2[0], idx3[0], idx4[0], idx5[0], idx6[0]))
    dst_pointcloud = np.delete(pointcloud, idx, 0)
    return dst_pointcloud


def pcl_view_pointcloud(point_cloud):
    """点云显示"""
    cloud = pcl.PointCloud_PointXYZRGBA()
    cloud.from_array(point_cloud)
    viewer = pcl.pcl_visualization.CloudViewing()
    viewer.ShowColorACloud(cloud)
    v = True
    while v:
        v = not (viewer.WasStopped())
