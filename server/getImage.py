import cv2
import gmpy2
import numpy
import matplotlib.pyplot as plt
import matplotlib
import os


class GetImage():
    def __init__(self):
        super().__init__()

    def image_generate(self, histogramPath, x, y):

        #matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        #matplotlib.rcParams['font.family'] = 'sans-serif'
        plt.figure(figsize=(16, 12), dpi=80)
        a = x

        # 计算组距
        d = 10000  # 组距
        num_bins = (max(a) - min(a)) // d

        """
        print('最大值：', max(a))
        print('最小值：', min(a))
        print('组距：', d)
        print('组数：', num_bins)
        绘制直方图
        data:必选参数，绘图数据
        bins:直方图的长条形数目，可选项，默认为10
        normed:是否将得到的直方图向量归一化，可选项，默认为0，代表不归一化，显示频数。normed=1，表示归一化，显示频率。
        facecolor:长条形的颜色
        edgecolor:长条形边框的颜色
        alpha:透明度
        """
        # plt.hist(data, bins=40, normed=0, facecolor="blue", edgecolor="black", alpha=0.7)

        lst = plt.hist(a, num_bins, density='True')
        #x = lst[1]
        #y = lst[0]
        # 设置数字标签
        # for x1,y1 in zip(x,y):
        #     plt.text(x1+1.5, y1+0.0005, '%.4f' % y1, ha='center', va= 'bottom',fontsize=12,rotation=-90,color='blue')
        # 设置x轴的刻度
        # plt.xticks(range(min(a), max(a) + d, d))
        #plt.grid()  # 画网格
        #plt.xlabel('区间')
        #plt.ylabel('频率/组距')
        plt.title(y)
        plt.savefig(histogramPath+"-"+y)



    # 生成差分直方图
    def generate_difference_histogram(self, cd1, cd2, cd3, cd4, cd5, cd6, filename):
        (name, ext) = os.path.splitext(filename)
        histogramPath = "./server/histogramImage/"+name
        GetImage.image_generate(self, histogramPath, cd1, "cd1")
        GetImage.image_generate(self, histogramPath, cd2, "cd2")
        GetImage.image_generate(self, histogramPath, cd3, "cd3")
        GetImage.image_generate(self, histogramPath, cd4, "cd4")
        GetImage.image_generate(self, histogramPath, cd5, "cd5")
        GetImage.image_generate(self, histogramPath, cd6, "cd6")
        print("直方图绘制完成")


    # 计算差分数据
    def calculate_difference_histogram(self, filename, encryptoimagepath, pixel, n, g, r):
        img = cv2.imread(encryptoimagepath)
        encrypto_image = img.copy()
        img_shape = img.shape
        # print("图片大小：", img_shape)
        height = int(img_shape[0])
        width = int(img_shape[1])
        pixel1 = numpy.zeros((height, width), dtype=numpy.int)
        # 获取加密后的像素值
        for i in range(img_shape[0]):
            for j in range(img_shape[1]):
                #pixel1[i][j] = int(encrypto_image[i, j][0]) * 65536 + int(encrypto_image[i, j][1]) * 256 + int(encrypto_image[i, j][2])
                pixel1[i][j] = pixel[i][j]

        # 差分计算cd1-cd6
        blockWidth = width // 5
        blockHeight = height // 5
        cd1 = numpy.zeros((blockHeight * blockWidth), dtype=numpy.int)
        cd2 = numpy.zeros((blockHeight * blockWidth), dtype=numpy.int)
        cd3 = numpy.zeros((blockHeight * blockWidth), dtype=numpy.int)
        cd4 = numpy.zeros((blockHeight * blockWidth), dtype=numpy.int)
        cd5 = numpy.zeros((blockHeight * blockWidth), dtype=numpy.int)
        cd6 = numpy.zeros((blockHeight * blockWidth), dtype=numpy.int)
        k = int(0)
        for i in range(blockHeight):
            for j in range(blockWidth):
                x_2_y_2 = int(pixel[5*i][5*j])
                x2y_2 = int(pixel[5*i][5*j+4])
                x_2y2 = int(pixel[5*i+4][5*j])
                x2y2 = int(pixel[5*i+4][5*j+4])
                xy = int(pixel[5*i+2][5*j+2])
                xy_ni = gmpy2.invert(xy, n**2)
                xy_2 = int(pixel[5*i+2][5*j])
                x_2y = int(pixel[5*i][5*j+2])
                x2y = int(pixel[5*i+4][5*j+2])
                x2y_ni = gmpy2.invert(x2y, n**2)
                xy2 = int(pixel[5*i+2][5*j+4])
                xy2_ni = gmpy2.invert(xy2, n**2)

                cd1[k] = (x_2_y_2 * xy2_ni) % n**2
                cd2[k] = (x2y_2 * xy_ni) % n**2
                cd3[k] = (x_2y2 * xy_ni) % n**2
                cd4[k] = (x2y2 * xy_ni) % n**2
                cd5[k] = (xy_2 * xy2_ni) % n**2
                cd6[k] = (x_2y * x2y_ni) % n**2
                k = k + 1

        print("开始绘制直方图")
        GetImage.generate_difference_histogram(self, cd1, cd2, cd3, cd4, cd5, cd6, filename)
        #for i in range(k):
        #    print(cd1[i])




    # 进行生成差方直方图步骤
    def get_image(self, filename, encryptoimagepath, pixel, n, g, r):
        print("server:")
        print("开始求差分")
        GetImage.calculate_difference_histogram(self, filename, encryptoimagepath, pixel, n, g, r)

