# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 17:51:43 2023

@author: 23818
"""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QDoubleSpinBox, QSpacerItem, QSizePolicy, QMessageBox)

def process_atlas_files(folder_path, scale_factor):
    processed_files = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".atlas"):
            new_filename = filename.replace(".atlas", ".txt")
            try:
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
                os.rename(os.path.join(folder_path, new_filename), os.path.join(folder_path, filename))
                processed_files += 1
            except Exception as e:
                return f"在处理 {filename} 时出错: {str(e)}"
    return f"已成功修改 {processed_files} 个 .atlas 文件并保存在原文件夹中！"

class AtlasModifierApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.folder_label = QLabel("文件夹路径：")
        self.folder_entry = QLineEdit(self)
        self.browse_button = QPushButton("浏览", self)
        self.browse_button.clicked.connect(self.browse_folder)

        self.scale_label = QLabel("放大倍数：")
        self.scale_entry = QDoubleSpinBox(self)
        self.scale_entry.setValue(1)
        self.scale_entry.setRange(0.1, 20)
        self.scale_entry.setSingleStep(0.1)

        self.process_button = QPushButton("处理文件", self)
        self.process_button.clicked.connect(self.process_files)
        self.result_label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_entry)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.scale_label)
        layout.addWidget(self.scale_entry)
        layout.addWidget(self.process_button)
        layout.addWidget(self.result_label)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setWindowTitle("Atlas文件修改器")
        self.resize(400, 250)

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "请选择文件夹")
        if folder_path:
            self.folder_entry.setText(folder_path)

    def process_files(self):
        folder_path = self.folder_entry.text()
        if not folder_path:
            QMessageBox.warning(self, '警告', '请选择一个文件夹!')
            return
        scale_factor = self.scale_entry.value()
        result = process_atlas_files(folder_path, scale_factor)
        self.result_label.setText(result)


app = QApplication(sys.argv)
window = AtlasModifierApp()
window.show()
sys.exit(app.exec_())
