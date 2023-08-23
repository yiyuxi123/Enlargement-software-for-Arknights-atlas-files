
import sys
import os
import re
import shutil
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QDoubleSpinBox, QSpacerItem, QSizePolicy, QMessageBox, QTextEdit, QProgressBar)

def process_atlas_files_optimized(folder_path, scale_factor):
    error_files = []
    processed_files = 0
    pattern = re.compile(r"(size|xy|orig):([\d.,\s]+)")
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".atlas"):
            backup_filename = filename.replace(".atlas", ".backup.atlas")
            shutil.copy(os.path.join(folder_path, filename), os.path.join(folder_path, backup_filename))
            new_filename = filename.replace(".atlas", ".txt")
            try:
                with open(os.path.join(folder_path, filename), "r") as f1, open(os.path.join(folder_path, new_filename), "w") as f2:
                    for line in f1:
                        match = pattern.search(line)
                        if match:
                            key, values = match.groups()
                            new_values = [str(int(float(value) * scale_factor)) if value.strip().replace('.', '', 1).isdigit() else value for value in values.strip().split(",")]
                            f2.write(f'{key}: {",".join(new_values)}\n')
                        else:
                            f2.write(line)
                os.remove(os.path.join(folder_path, filename))
                os.rename(os.path.join(folder_path, new_filename), os.path.join(folder_path, filename))
                processed_files += 1
            except Exception as e:
                error_files.append((filename, str(e)))
    if error_files:
        return f"以下文件处理时出错:\n" + "\n".join([f"{file}: {error}" for file, error in error_files])
    return f"已成功修改 {processed_files} 个 .atlas 文件并保存在原文件夹中！"

class AtlasModifierAppOptimized(QMainWindow):
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
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        layout = QVBoxLayout()
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_entry)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.scale_label)
        layout.addWidget(self.scale_entry)
        layout.addWidget(self.process_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.result_text)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle("Atlas文件修改器")
        self.resize(400, 300)

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "请选择文件夹")
        if folder_path:
            self.folder_entry.setText(folder_path)

    def process_files(self):
        folder_path = self.folder_entry.text()
        if not folder_path:
            QMessageBox.warning(self, '警告', '请选择一个文件夹!')
            return
        self.progress_bar.setValue(0)
        self.result_text.clear()
        scale_factor = self.scale_entry.value()
        result = process_atlas_files_optimized(folder_path, scale_factor)
        self.progress_bar.setValue(100)
        self.result_text.setText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AtlasModifierAppOptimized()
    window.show()
    sys.exit(app.exec_())
