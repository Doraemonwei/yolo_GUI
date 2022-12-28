import os
from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog, QLabel, QWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon, QImage, QPixmap
from PySide2 import QtCore
from PySide2.QtCore import QTimer, QSize, Signal, QObject
import cv2
from yolo import detect
import threading


# 自定义信号源对象类型，用来感知yolo处理的状态
class MySignals(QObject):
    # emit(0)表示是视频，1 表示是图片
    yolo_state = Signal(int)
    # 当yolo正在处理的时候关掉按钮
    button_state = Signal()


_state = MySignals()


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        self.ui = QUiLoader().load('qt/window.ui')

        self.ui.setWindowIcon(QIcon('qt/微波炉.png'))
        # 绑定各个按钮点击时的操作函数
        self.ui.pushButton.clicked.connect(self.image_button_clicked)
        self.ui.pushButton_2.clicked.connect(self.video_button_clicked)
        # 初始化一些全局的变量
        #    待处理对象的绝对路径
        self.file_path = None

        # 定义一个信号，用来判断yolo是否处理完毕
        _state.yolo_state.connect(self.check_video_image_model)
        _state.button_state.connect(self.change_button_state)

        # 使用的模型
        self.model_name = r'yolo/yolov5s.pt'
        self.ui.model_comboBox.activated[str].connect(self.choose_model)

    def check_video_image_model(self, kind):
        if kind == 0:
            self.show_image()
        else:
            self.play_video()

    def image_button_clicked(self):
        self.file_path = self.open_file("图片")
        if not self.file_path:
            return
        if not self.model_name:
            QMessageBox.critical(self.ui, '警告', '请选择模型!')
            return
        self.ui.label.setText('YOLO处理中......')
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)

        th = threading.Thread(target=self.yolo_detect, args=(0,))
        th.start()

    def video_button_clicked(self):
        self.file_path = self.open_file("视频")
        if not self.file_path:
            return

        if not self.model_name:
            QMessageBox.critical(self.ui, '警告', '请选择模型!')
            return
        self.ui.label.setText('YOLO处理中......')
        th = threading.Thread(target=self.yolo_detect, args=(1,))
        th.start()

    def model_button_clicked(self):
        pass

    def open_file(self, file_type):
        """
        弹出一个只能打开图片的对话框，用户选择图片，记住路径
        """
        # 生成文件对话框对象
        fileName = 'image'

        if file_type == '图片':
            fileName, _ = QFileDialog.getOpenFileName(self.ui, "选择图片", "",
                                                      "*.jpg;;*.png;;*.jpeg")
        if file_type == '视频':
            fileName, _ = QFileDialog.getOpenFileName(self.ui, "选择视频", "",
                                                      "*.mp4;;*.avi")
        if file_type == '模型':
            fileName, _ = QFileDialog.getOpenFileName(self.ui, "选择模型", "",
                                                      "*.mp4;;*.avi")
        if fileName:
            return fileName
        else:
            QMessageBox.critical(self.ui, '警告', '请选择{}!'.format(file_type))

    def show_image(self):
        # 通过self.file_path对应的yolo处理之后的路径 来在 label 上显示图片
        (path, filename) = os.path.split(self.file_path)
        detected_image_path = os.path.join(path, 'exp', filename)
        cv_img = cv2.imread(detected_image_path, -1)
        height, width, channel = cv_img.shape
        bytesPerline = 3 * width
        qImg = QImage(cv_img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
        # 缩放以适应窗口大小，由于label.size()包含了显示区域和边界，因此要减去两边各1像素的边界
        pixmap = QPixmap.fromImage(qImg)
        pixmap = pixmap.scaled(self.ui.label.size() - QSize(2, 2))  # 保证图片大小适应窗口
        # 在label上显示图像
        self.ui.label.setPixmap(pixmap)

    def play_video(self):
        # 通过self.file_path对应的yolo处理之后的路径 来在 label 上显示视频
        (path, filename) = os.path.split(self.file_path)
        video_path = os.path.join(path, 'exp', filename)
        cap = cv2.VideoCapture(video_path)
        if not cap:
            QMessageBox.critical(self.ui, '警告', '打开视频失败！')
            return
        # 获取视频FPS
        fps = cap.get(cv2.CAP_PROP_FPS)
        # 设置时钟
        v_timer = QTimer(self.ui)

        def show_frame():
            success, frame = cap.read()
            if success:
                # Mat格式图像转Qt中图像的方法
                show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(showImage)
                # window是是实例化之后主窗口的名称
                pixmap = pixmap.scaled(self.ui.label.size() - QSize(2, 2))  # 保证图片大小适应窗口
                self.ui.label.setPixmap(pixmap)
            else:
                v_timer.stop()

        print("启动计时器开始播放视频...")
        v_timer.timeout.connect(show_frame)
        v_timer.start(int(1000 / fps))

    def yolo_detect(self, kind):
        (path, filename) = os.path.split(self.file_path)
        detect.parse_opt(self.file_path, path, self.model_name)
        _state.yolo_state.emit(kind)
        _state.button_state.emit()

    def choose_model(self):
        self.model_name = os.path.join('yolo', self.ui.model_comboBox.currentText() + '.pt')
        print('已选择模型路径为：{}'.format(self.model_name))

    def change_button_state(self):
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(True)


if __name__ == "__main__":
    # 保证窗口大小一致
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication([])
    app.setStyle('windows')  # 设置 windows 风格

    window = MainWindow()
    window.ui.show()
    app.exec_()
