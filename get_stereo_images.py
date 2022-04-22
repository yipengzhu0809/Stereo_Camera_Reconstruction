# -*-coding: utf-8 -*-


import os
import argparse
import cv2


class StereoCamera(object):
    """采集双目标定图片，按键盘【c】或【s】保存图片"""

    def __init__(self, chess_width, chess_height, detect=False):
        """
        :param chess_width: chessboard width size，即棋盘格宽方向黑白格子相交点个数，
        :param chess_height: chessboard height size，即棋盘格长方向黑白格子相交点个数
        :param detect: 是否实时检测棋盘格，方便采集数据
        """
        self.chess_width = chess_width
        self.chess_height = chess_height
        self.detect = detect
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def detect_chessboard(self, image):
        """检测棋盘格"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (self.chess_width, self.chess_height), None)
        if ret:
            # 角点精检测
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
            # Draw and display the corners
            image = cv2.drawChessboardCorners(image, (self.chess_width, self.chess_height), corners2, ret)
        return image

    def capture2(self, left_video, right_video, save_dir):
        """
        用于采集双USB连接线的双目摄像头
        :param left_video:int or str,左路视频路径或者摄像头ID
        :param right_video:int or str,右视频路径或者摄像头ID
        :param save_dir: str,保存左右图片的路径
        :return:
        """
        self.create_file(save_dir)
        capL = cv2.VideoCapture(left_video)
        capR = cv2.VideoCapture(right_video)
        widthL, heightL, numFramesL, fpsL = self.get_video_info(capL)
        widthR, heightR, numFramesR, fpsR = self.get_video_info(capR)
        print("capL:\n", widthL, heightL, numFramesL, fpsL)
        print("capR:\n", widthR, heightR, numFramesR, fpsR)
        save_videoL = self.create_file(save_dir, "video", "left_video.avi")
        save_videoR = self.create_file(save_dir, "video", "right_video.avi")
        writerL = self.get_video_writer(save_videoL, widthL, heightL, fpsL)
        writerR = self.get_video_writer(save_videoR, widthR, heightR, fpsR)
        i = 0
        while True:
            isuccessL, frameL = capL.read()
            isuccessR, frameR = capR.read()
            if not (isuccessL and isuccessR):
                print("No more frames")
                break
            if self.detect:
                l = self.detect_chessboard(frameL.copy())
                r = self.detect_chessboard(frameR.copy())
            else:
                l = frameL.copy()
                r = frameR.copy()
            cv2.imshow('left', l)
            cv2.imshow('right', r)
            key = cv2.waitKey(10)
            if key == ord('q'):
                break
            elif key == ord('c') or key == ord('s'):
                print("save image:{:0=3d}".format(i))
                cv2.imwrite(os.path.join(save_dir, "left_{:0=3d}.png".format(i)), frameL)
                cv2.imwrite(os.path.join(save_dir, "right_{:0=3d}.png".format(i)), frameR)
                i += 1
            writerL.write(frameL)
            writerR.write(frameR)
        capL.release()
        capR.release()
        cv2.destroyAllWindows()

    def capture1(self, video, save_dir):
        """
        用于采集单USB连接线的双目摄像头(左右摄像头被拼接在同一个视频中显示)
        :param video:int or str,视频路径或者摄像头ID
        :param save_dir: str,保存左右图片的路径
        """
        self.create_file(save_dir)
        cap = cv2.VideoCapture(video)
        width, height, numFrames, fps = self.get_video_info(cap)
        print("capL:\n", width, height, numFrames, fps)
        save_videoL = self.create_file(save_dir, "video", "left_video.avi")
        save_videoR = self.create_file(save_dir, "video", "right_video.avi")
        writerL = self.get_video_writer(save_videoL, int(width / 2), height, fps)
        writerR = self.get_video_writer(save_videoR, int(width / 2), height, fps)
        i = 0
        while True:
            isuccess, frame = cap.read()
            if not isuccess:
                print("No more frames")
                break
            # 分离左右摄像头
            frameL = frame[:, :int(width / 2), :]
            frameR = frame[:, int(width / 2):, :]
            if self.detect:
                l = self.detect_chessboard(frameL.copy())
                r = self.detect_chessboard(frameR.copy())
            else:
                l = frameL.copy()
                r = frameR.copy()
            cv2.imshow('left', l)
            cv2.imshow('right', r)
            key = cv2.waitKey(10)
            if key == ord('q'):
                break
            elif key == ord('c') or key == ord('s'):
                print("save image:{:0=3d}".format(i))
                cv2.imwrite(os.path.join(save_dir, "left_{:0=3d}.png".format(i)), frameL)
                cv2.imwrite(os.path.join(save_dir, "right_{:0=3d}.png".format(i)), frameR)
                i += 1
            writerL.write(frameL)
            writerR.write(frameR)
        cap.release()
        cv2.destroyAllWindows()

    @staticmethod
    def get_video_info(video_cap):
        width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        numFrames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(video_cap.get(cv2.CAP_PROP_FPS))
        return width, height, numFrames, fps

    @staticmethod
    def get_video_writer(save_path, width, height, fps):
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        frameSize = (int(width), int(height))
        video_writer = cv2.VideoWriter(save_path, fourcc, fps, frameSize)
        print("video:width:{},height:{},fps:{}".format(width, height, fps))
        return video_writer

    @staticmethod
    def create_file(parent_dir, dir1=None, filename=None):
        out_path = parent_dir
        if dir1:
            out_path = os.path.join(parent_dir, dir1)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        if filename:
            out_path = os.path.join(out_path, filename)
        return out_path


def str2bool(v):
    return v.lower() in ('yes', 'true', 't', 'y', '1')


def get_parser():
    width = 8
    height = 11
    left_video = -1
    right_video = 0
    save_dir = "data/camera"
    parser = argparse.ArgumentParser(description='Camera calibration')
    parser.add_argument('--width', type=int, default=width, help='chessboard width size')
    parser.add_argument('--height', type=int, default=height, help='chessboard height size')
    parser.add_argument('--left_video', type=int, default=left_video, help='left video file or camera ID')
    parser.add_argument('--right_video', type=int, default=right_video, help='right video file or camera ID')
    parser.add_argument('--detect', type=str2bool, nargs='?', const=True, help='detect chessboard ')
    parser.add_argument('--save_dir', type=str, default=save_dir, help='YML file to save calibrate matrices')
    return parser


if __name__ == '__main__':
    args = get_parser().parse_args()
    stereo = StereoCamera(args.width, args.height, detect=args.detect)
    if args.left_video > -1 and args.right_video > -1:
        # 双USB连接线的双目摄像头
        stereo.capture2(left_video=args.left_video, right_video=args.right_video, save_dir=args.save_dir)
    elif args.left_video > -1:
        # 单USB连接线的双目摄像头(左右摄像头被拼接在同一个视频中显示)
        stereo.capture1(video=args.left_video, save_dir=args.save_dir)
    elif args.right_video > -1:
        # 单USB连接线的双目摄像头(左右摄像头被拼接在同一个视频中显示)
        stereo.capture1(video=args.right_video, save_dir=args.save_dir)
    else:
        raise Exception("Error: Check your camera{}".format(args.left_video, args.right_video))
