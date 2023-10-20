# 车牌识别
import time

import cv2 as cv
import numpy as np
import os


# 提取车牌（形态学）
def Morph_Distinguish(img,dist_far:bool):
    # 1、转灰度图
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    # 2、顶帽运算
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (17, 17))
    tophat = cv.morphologyEx(gray, cv.MORPH_TOPHAT, kernel)
    # cv.imshow('tophat', tophat)

    # 3、Sobel算子提取y方向边缘
    y = cv.Sobel(tophat, cv.CV_16S, 1, 0)
    absY = cv.convertScaleAbs(y)
    # cv.imshow('absY', absY)

    # 4、自适应二值化
    ret, binary = cv.threshold(absY, 75, 255, cv.THRESH_BINARY)
    # cv.imshow('binary', binary)

    # 5、开运算分割
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 15))
    Open = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
    # cv.imshow('Open', Open)

    # 6、闭运算合并，把图像闭合、揉团，使图像区域化，便于找到车牌区域，进而得到轮廓
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (41, 15))
    close = cv.morphologyEx(Open, cv.MORPH_CLOSE, kernel)
    # cv.imshow('close', close)

    # 7、膨胀/腐蚀
    # 中远距离车牌识别
    if dist_far:
        kernel_x = cv.getStructuringElement(cv.MORPH_RECT, (25, 7))
        kernel_y = cv.getStructuringElement(cv.MORPH_RECT, (1, 11))
    else:
        kernel_x = cv.getStructuringElement(cv.MORPH_RECT, (79, 15))
        kernel_y = cv.getStructuringElement(cv.MORPH_RECT, (1, 31))
    # 7-1、腐蚀、膨胀（去噪）
    erode_y = cv.morphologyEx(close, cv.MORPH_ERODE, kernel_y)
    # cv.imshow('erode_y', erode_y)
    dilate_y = cv.morphologyEx(erode_y, cv.MORPH_DILATE, kernel_y)
    # cv.imshow('dilate_y', dilate_y)
    # 7-1、膨胀、腐蚀（连接）（二次缝合）
    dilate_x = cv.morphologyEx(dilate_y, cv.MORPH_DILATE, kernel_x)
    # cv.imshow('dilate_x', dilate_x)
    erode_x = cv.morphologyEx(dilate_x, cv.MORPH_ERODE, kernel_x)
    # cv.imshow('erode_x', erode_x)

    # 8、腐蚀、膨胀：去噪
    kernel_e = cv.getStructuringElement(cv.MORPH_RECT, (25, 9))
    erode = cv.morphologyEx(erode_x, cv.MORPH_ERODE, kernel_e)
    # cv.imshow('erode', erode)
    kernel_d = cv.getStructuringElement(cv.MORPH_RECT, (25, 11))
    dilate = cv.morphologyEx(erode, cv.MORPH_DILATE, kernel_d)
    # cv.imshow('dilate', dilate)

    # 9、获取外轮廓
    img_copy = img.copy()
    # 9-1、得到轮廓
    contours, hierarchy = cv.findContours(dilate, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # 9-2、画出轮廓并显示
    cv.drawContours(img_copy, contours, -1, (255, 0, 255), 2)
    # cv.imshow('Contours', img_copy)
    cv.imwrite('CAR_RAW.jpg', img_copy)
    # 10、遍历所有轮廓，找到车牌轮廓
    i = 0
    ans=[]
    for contour in contours:
        # 10-1、得到矩形区域：左顶点坐标、宽和高
        rect = cv.boundingRect(contour)
        # 10-2、判断宽高比例是否符合车牌标准
        print(rect)
        if rect[2] > rect[3] * 3 and rect[2] < rect[3] * 7 and rect[2]>8 and rect[3]>15:
            # 截取车牌并显示
            ans.append(rect)

            if rect[0]>10:
                rect=(rect[0]-10,rect[1],rect[2],rect[3])
            if rect[1] > 10:
                rect = (rect[0] , rect[1]- 10, rect[2], rect[3])
            imgx = img[(rect[1] ):(rect[1] + rect[3]+30 ), (rect[0]):(rect[0] + rect[2]+30 )]  # 高，宽
            try:
                # cv.imshow('CAR_'+str(i), imgx)
                cv.imwrite('plate/CAR_'+str(i)+'.jpg', imgx)
            except:
                pass
            i += 1
    return ans

def Getmask(paths):
    s = os.listdir("plate/")
    for name in s:
        os.remove("plate/"+name)
    path=paths
    img = cv.imread(path)
    arr=Morph_Distinguish(img,True)  # 形态学提取车牌
    i=0
    if len(arr)==0:
        return -1
    for index,tmp in enumerate(arr):
        if tmp[2]>arr[i][2] and tmp[3]>arr[i][3]:
            i=index
    return i


def resize_image(input_path, new_width, new_height):
    try:
        # 读取输入图片
        image = cv.imread(input_path)

        # 缩放图片
        resized_image = cv.resize(image, (new_width, new_height))

        # 保存缩放后的图片
        cv.imwrite(input_path, resized_image)

        print("Image resized and saved successfully.")
    except Exception as e:
        print("An error occurred:", str(e))
# Getmask("cap_raw.jpg")