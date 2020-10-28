# -*- coding: utf-8 -*
"""运行客户端"""
import _thread
import tkinter as tk
from tkinter import messagebox
from client.upload import Application
import client.generateKays

def run():
    root = tk.Tk()
    root.title("Upload")
    root.geometry("400x100+600+300")
    app = upload.Application(master=root)
    app.mainloop()

def generate_kay():
    generateKays.main()