# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 01:21:45 2023

@author: 23818
"""
import os
import tkinter as tk
from tkinter import filedialog, ttk


def process_files():
    folder_path = folder_entry.get()
    scale_factor = float(scale_entry.get())

    for filename in os.listdir(folder_path):
        if filename.endswith(".atlas"):
            new_filename = filename.replace(".atlas", ".txt")
            with open(os.path.join(folder_path, filename), "r") as f1, \
                    open(os.path.join(folder_path, new_filename), "w") as f2:
                for line in f1:
                    if "size" in line or "xy" in line or "orig" in line:
                        parts = line.split(":")
                        if len(parts) == 2:
                            new_values = [str(int(float(value) * scale_factor)) if value.strip().replace('.', '', 1).isdigit() else value for value in parts[1].strip().split(",")]
                            f2.write(f'{parts[0]}: {",".join(new_values)}\n')
                        else:
                            f2.write(line)
                    else:
                        f2.write(line)

            os.remove(os.path.join(folder_path, filename))
            os.rename(os.path.join(folder_path, new_filename),
                      os.path.join(folder_path, filename))

    result_label.config(text="文件夹内后缀为 .atlas 的文件已经被成功修改并保存在原文件夹中！")


def browse_folder():
    folder_path = filedialog.askdirectory(title="请选择文件夹")
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)


root = tk.Tk()
root.title("Atlas文件修改器")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

folder_label = ttk.Label(frame, text="文件夹路径：")
folder_label.grid(row=0, column=0, sticky=tk.W)

folder_entry = ttk.Entry(frame, width=50)
folder_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

browse_button = ttk.Button(frame, text="浏览", command=browse_folder)
browse_button.grid(row=0, column=2, sticky=tk.W)

scale_label = ttk.Label(frame, text="放大倍数：")
scale_label.grid(row=1, column=0, sticky=tk.W)

scale_entry = ttk.Entry(frame, width=10)
scale_entry.grid(row=1, column=1, sticky=tk.W)

process_button = ttk.Button(frame, text="处理文件", command=process_files)
process_button.grid(row=2, column=1, pady=10)

result_label = ttk.Label(frame, text="")
result_label.grid(row=3, column=1, sticky=tk.W)

frame.columnconfigure(1, weight=1)

root.mainloop()
