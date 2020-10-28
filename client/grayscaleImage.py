import cv2
import tkinter as tk
import os
import numpy
from client.encryptImage import Encrypt



class GenerateGrayscale():
    def __init__(self):
        super().__init__()

    def gray_mean_rgb(self, inputimagepath, grayscaleoutimagepath, filename):
        img = cv2.imread(inputimagepath)
        gray_mean_rgb_image = img.copy()
        img_shape = img.shape
        # print("图片大小：", img_shape)
        height = int(img_shape[0])
        width = int(img_shape[1])
        pixel = numpy.zeros((height, width), dtype=numpy.int)
        for i in range(img_shape[0]):
            for j in range(img_shape[1]):
                pixel[i][j] = gray_mean_rgb_image[i, j] = (int(img[i, j][0]) + int(img[i, j][1]) + int(img[i, j][2])) / 3

        cv2.imwrite(grayscaleoutimagepath, gray_mean_rgb_image)  # 保存当前灰度值处理过后的文件
        # 调用加密模块
        print("跳转至加解密模块")
        Encrypt.image_paillier(self, grayscaleoutimagepath, filename, height, width, pixel)

    def generate_grayscale(self, filePath):
        (path, filename) = os.path.split(filePath)
        inputimagepath = filePath
        grayscaleoutimagepath = "./client/grayscaleImage/"+filename
        GenerateGrayscale.gray_mean_rgb(self, inputimagepath, grayscaleoutimagepath, filename)