from gmpy2 import powmod
import cv2
import shutil
from PIL import Image
from server.getImage import GetImage

class Encrypt():
    def __init__(self):
        super().__init__()

    def L(self, x, n):
        return (self, x - 1) // n

    # 加密图片
    def pailllier_encrypto(self, grayscaleimagepath, encryptoimagepath, height, width, pixel):
        # 读取公私钥
        list_pub = [0, 0, 0]
        i = 0
        for line in open("./client/keys/pub.txt"):
            list_pub[i] = int(line)
            i = i + 1
        n = list_pub[0]
        g = list_pub[1]
        r = list_pub[2]
        print("公钥：n =", n, "g =", g, "r =", r)

        # 加密生成新图片
        R = int(0)
        G = int(0)
        B = int(0)
        img = cv2.imread(grayscaleimagepath)
        encrypto_image = img.copy()
        for i in range(height):
            for j in range(width):
                m = int(pixel[i][j])
                a = powmod(g, m, n ** 2)
                b = powmod(r, n, n ** 2)
                pixel[i][j] = int((a * b) % (n ** 2))
                # print(pixel[i][j])
                R = pixel[i][j] // 65536
                G = (pixel[i][j] % 65536) // 256
                B = (pixel[i][j] % 65536) % 256
                # print(R, G, B)
                encrypto_image[i, j][0] = R
                encrypto_image[i, j][1] = G
                encrypto_image[i, j][2] = B
        cv2.imwrite(encryptoimagepath, encrypto_image)
        print("加密完成")

    # 解密图片
    def paillier_decrypto(self, encryptoimagepath, decryptoimagepath, height, width, pixel):
        # 读取私钥
        list_pri = [0, 0, 0]
        i = 0
        for line in open("./client/keys/pri.txt"):
            list_pri[i] = int(line)
            i = i + 1
        n = list_pri[0]
        l = list_pri[1]
        u = list_pri[2]
        print("私钥：n =", n, "l =", l, "u =", u)
        img2 = cv2.imread(encryptoimagepath)
        decrypto_image = img2.copy()
        img3 = Image.new("RGB", (width, height))
        for i in range(height):
            for j in range(width):
                R = int(decrypto_image[i, j][0])
                G = int(decrypto_image[i, j][1])
                B = int(decrypto_image[i, j][2])
                # print(R,G,B)
                temp = pixel[i][j]
                #temp = B + 256 * G + 65536 * R
                #if temp == pixel[i][j]:
                #    print(temp,i,j)
                c = int(temp) % n ** 2
                a = powmod(c, l, n ** 2)
                decryptoPixel = ((a - 1) // n) * u % n
                img3.putpixel((j, i), (int(decryptoPixel), int(decryptoPixel), int(decryptoPixel)))
        img3.save(decryptoimagepath)
        print("解密完成")

    def image_paillier(self, grayscaleimagepath, filename, height, width, pixel):
        # 加密
        print("加密中······")
        encryptoimagepath = "./client/encryptoImage/" + filename
        Encrypt.pailllier_encrypto(self, grayscaleimagepath, encryptoimagepath, height, width, pixel)

        # 解密
        print("解密中······")
        decryptoimagepath = "./client/decryptoImage/" + filename
        Encrypt.paillier_decrypto(self, encryptoimagepath, decryptoimagepath, height, width, pixel)

        # 将加密后的像素点传到服务器端
        print("加密后的图像传至server端")
        shutil.copyfile(encryptoimagepath, "./server/encryptoImage/" + filename)

        # 跳转至server
        # 读取公私钥
        list_pub = [0, 0, 0]
        i = 0
        for line in open("./client/keys/pub.txt"):
            list_pub[i] = int(line)
            i = i + 1
        n = list_pub[0]
        g = list_pub[1]
        r = list_pub[2]
        print("跳转至server端")
        GetImage.get_image(self, filename, encryptoimagepath, pixel, n, g, r)
