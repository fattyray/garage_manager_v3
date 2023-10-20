import cv2
import numpy as np


def Getimg(width: int, height: int):
    cv2.namedWindow("Photo_Detect")  # 定义一个窗口
    cap = cv2.VideoCapture(0)  # 捕获摄像头图像  0位默认的摄像头 笔记本的自带摄像头  1为外界摄像头
    # 值为1不断读取图像
    ret, frame = cap.read()  # 视频捕获帧
    cv2.imwrite('cap_raw.jpg', frame)  # 写入捕获到的视频帧  命名为
    # cv2.imshow('Photo_Detect', frame)  # 显示窗口 查看实时图像
    img = cv2.resize(frame, (width, height))  # 图像大小为640*480
    # cv2.imshow('cap_final_img', img)
    cv2.imwrite('cap.jpg', img)
    # 执行完后释放窗口
    cap.release()
    # cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True


# Getimg(800, 600)
