# -*-coding: utf-8 -*-


import cv2


def detect_chessboard(image, chess_width=8, chess_height=11):
    """检测棋盘格"""
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (chess_width, chess_height), None)
    if ret:
        # 角点精检测
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        # Draw and display the corners
        image = cv2.drawChessboardCorners(image, (chess_width, chess_height), corners2, ret)
    return image


if __name__ == '__main__':
    image_file = "/home/dm/data3/Project/3D/Camera-Calibration-Reconstruct/docs/right_003.png"
    image = cv2.imread(image_file)
    image = detect_chessboard(image)
    cv2.imwrite("../docs/right_chess.png", image)
