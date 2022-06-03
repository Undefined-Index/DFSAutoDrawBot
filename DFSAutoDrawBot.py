import os
import time
import sys
from PIL import Image, ImageFilter
import pyautogui
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

sys.setrecursionlimit(2000)  # 递归次数限制

pic_path = 'pic.jpg'  # 图片路径
alpha = 0.05  # 高斯核标准差
winSize = 21  # 高斯核大小
draw_delay = 0.001  # 绘制延迟
jd = 1  # 绘制精度
gl = 200  # 灰度过滤阈值


def busy_sleep():  # 高精度sleep
    start = time.time()
    while (time.time() < start + draw_delay):
        pass


def mouse_up_judge(xx, yy):  # 判断下一个像素点是否远距离偏移
    position_x, position_y = pyautogui.position()
    if position_x - jd != xx and position_x + jd != xx and position_y + jd != yy and position_y - jd != yy:
        pyautogui.mouseUp()
        return True
    else:
        return False


def dfs(img, x, y, first, count=0):
    if count >= 1900:  #避免超过python递归极限报错
        return [x, y]
    count += 1

    if first == True:
        pyautogui.moveTo(width + y, height + x, 0)
        pyautogui.mouseDown()

    if y + jd < cols and x - jd >= 0:
        if img[x - jd, y + jd] == 0:
            mouse_judge = mouse_up_judge(width + y + jd, height + x - jd)
            pyautogui.moveTo(width + y + jd, height + x - jd)
            if mouse_judge == True:
                pyautogui.mouseDown()
            img[x - jd, y + jd] = 1
            busy_sleep()
            dfs(img, x - jd, y + jd, False, count)

    if y + jd < cols and x + jd < rows:
        if img[x + jd, y + jd] == 0:
            mouse_judge = mouse_up_judge(width + y + jd, height + x + jd)
            pyautogui.moveTo(width + y + jd, height + x + jd)
            if mouse_judge == True:
                pyautogui.mouseDown()
            img[x + jd, y + jd] = 1
            busy_sleep()
            dfs(img, x + jd, y + jd, False, count)

    if y - jd >= 0 and x - jd >= 0:
        if img[x - jd, y - jd] == 0:
            mouse_judge = mouse_up_judge(width + y - jd, height + x - jd)
            pyautogui.moveTo(width + y - jd, height + x - jd)
            if mouse_judge == True:
                pyautogui.mouseDown()
            img[x - jd, y - jd] = 1
            busy_sleep()
            dfs(img, x - jd, y - jd, False, count)

    if y - jd >= 0 and x + jd < rows:
        if img[x + jd, y - jd] == 0:
            mouse_judge = mouse_up_judge(width + y - jd, height + x + jd)
            pyautogui.moveTo(width + y - jd, height + x + jd)
            if mouse_judge == True:
                pyautogui.mouseDown()
            img[x + jd, y - jd] = 1
            busy_sleep()
            dfs(img, x + jd, y - jd, False, count)

    if y + jd < cols:
        if img[x, y + jd] == 0:
            mouse_judge = mouse_up_judge(width + y + jd, height + x)
            pyautogui.moveTo(width + y + jd, height + x)
            if mouse_judge == True:
                pyautogui.mouseDown()
            img[x, y + jd] = 1
            busy_sleep()
            dfs(img, x, y + jd, False, count)

    if y - jd >= 0:
        if img[x, y - jd] == 0:
            mouse_judge = mouse_up_judge(width + y - jd, height + x)
            pyautogui.moveTo(width + y - jd, height + x)
            if mouse_judge == True:
                pyautogui.mouseDown()
            img[x, y - jd] = 1
            busy_sleep()
            dfs(img, x, y - jd, False, count)

    if x - jd >= 0:
        if img[x - jd, y] == 0:
            mouse_judge = mouse_up_judge(width + y, height + x - jd)
            pyautogui.moveTo(width + y, height + x - jd)
            if mouse_judge == True:
                pyautogui.mouseDown()
            img[x - jd, y] = 1
            busy_sleep()
            dfs(img, x - jd, y, False, count)

    if x + jd < rows:
        if img[x + jd, y] == 0:
            mouse_judge = mouse_up_judge(width + y, height + x + jd)
            pyautogui.moveTo(width + y, height + x + jd)
            if mouse_judge == True:
                pyautogui.mouseDown()
            img[x + jd, y] = 1
            busy_sleep()
            dfs(img, x + jd, y, False, count)
    return None


if __name__ == '__main__':
    img = cv.imread(pic_path, 0)  # img path
    img_blur = cv.GaussianBlur(img, (winSize, winSize), 5)
    img = np.uint8(img > (1 - alpha) * img_blur) * 255
    cv.imwrite("temp_img.jpg", img)
    img = Image.open('temp_img.jpg')

    # 修改图片尺寸
    width = img.size[0]
    height = img.size[1]
    if width > 1600 or height > 1600:
        img = img.resize((int(width * 0.4), int(height * 0.4)))
    elif width > 1200 or height > 1200:
        img = img.resize((int(width * 0.5), int(height * 0.5)))
    elif width > 1000 or height > 1000:
        img = img.resize((int(width * 0.6), int(height * 0.6)))
    elif width > 800 or height > 800:
        img = img.resize((int(width * 0.7), int(height * 0.7)))

    # 图片处理
    img = img.convert('L')
    img = np.array(img)
    rows, cols = img.shape
    for i in range(rows):
        for j in range(cols):
            if img[i, j] <= gl:
                img[i, j] = 0
            else:
                img[i, j] = 1

    img = Image.fromarray(img)
    img = img.filter(ImageFilter.SMOOTH)
    img = np.array(img)

    plt.figure("lena")  # 预览图
    plt.imshow(img, cmap='gray')
    plt.axis('off')
    plt.show()

    input("start?")
    time.sleep(3)
    pyautogui.PAUSE = 0

    height = 1080 / 2 - rows / 2
    width = 1920 / 2 - cols / 2

    count_i = 0
    while count_i < rows:
        count_j = 0
        while count_j < cols:
            if count_j + jd < cols:
                if img[count_i, count_j] == 0:
                    dfs_result = dfs(img, count_i, count_j, True, 0)
                    while dfs_result != None:
                        pyautogui.mouseUp()
                        dfs_result = dfs(img, dfs_result[0], dfs_result[1], True, 0)
                    pyautogui.mouseUp()
            count_j += jd
        count_i += jd
    os.remove('temp_img.jpg')
