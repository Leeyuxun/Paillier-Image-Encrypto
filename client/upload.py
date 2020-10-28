import tkinter as tk
from tkinter import filedialog
# from PIL import Image, ImageTk
from client.grayscaleImage import GenerateGrayscale
import shutil
import os


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.filePath = tk.StringVar()
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # 获取图片
        self.getFile_bt = tk.Button(self, text="Choose Image", command=self.get_filePath, width=38, height=1, fg="red", bg="sky blue")
        self.getFile_bt.pack(side="top")

        # 显示图片路径
        self.filePath_en = tk.Entry(self, width=40)
        self.filePath_en.pack(side="top")
        self.filePath_en.delete(0, "end")
        self.filePath_en.insert(0, "Please choose one image")

        self.getFile_bt = tk.Button(self, text="Upload Image", command=self.go_to_grayscale, width=38, height=1, fg="black", bg="sky blue")
        self.getFile_bt.pack(side="top")

    # 打开文件并显示路径
    def get_filePath(self):
        default_dir = r"文件路径"
        self.filePath = tk.filedialog.askopenfilename(title=u'选择文件', filetypes=[("便携式网络图形", "*.png"), ('破坏性图像格式', '*.jpg'),('破坏性图像格式', '*.jpeg')])
        print("client:")
        print("文件路径：", self.filePath)
        (path, filename) = os.path.split(self.filePath)
        shutil.copyfile(self.filePath, "./client/originalImage/"+filename)
        self.filePath_en.delete(0, "end")
        self.filePath_en.insert(0, self.filePath)

    def go_to_grayscale(self):
        print("进入图片处理阶段")
        GenerateGrayscale.generate_grayscale(self, self.filePath)