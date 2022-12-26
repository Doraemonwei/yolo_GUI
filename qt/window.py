# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_yolo_detect(object):
    def setupUi(self, yolo_detect):
        if not yolo_detect.objectName():
            yolo_detect.setObjectName(u"yolo_detect")
        yolo_detect.resize(639, 524)
        self.centralwidget = QWidget(yolo_detect)
        self.centralwidget.setObjectName(u"centralwidget")
        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(20, 110, 141, 321))
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.image_detect_button = QPushButton(self.widget_2)
        self.image_detect_button.setObjectName(u"image_detect_button")

        self.verticalLayout.addWidget(self.image_detect_button)

        self.video_view_button = QPushButton(self.widget_2)
        self.video_view_button.setObjectName(u"video_view_button")

        self.verticalLayout.addWidget(self.video_view_button)

        self.Model_view_button = QPushButton(self.widget_2)
        self.Model_view_button.setObjectName(u"Model_view_button")

        self.verticalLayout.addWidget(self.Model_view_button)

        self.image_label = QLabel(self.centralwidget)
        self.image_label.setObjectName(u"image_label")
        self.image_label.setGeometry(QRect(190, 50, 421, 431))
        self.image_label.setFrameShape(QFrame.Box)
        yolo_detect.setCentralWidget(self.centralwidget)

        self.retranslateUi(yolo_detect)

        QMetaObject.connectSlotsByName(yolo_detect)
    # setupUi

    def retranslateUi(self, yolo_detect):
        yolo_detect.setWindowTitle(QCoreApplication.translate("yolo_detect", u"\u56fe\u50cf\u8bc6\u522b", None))
        self.image_detect_button.setText(QCoreApplication.translate("yolo_detect", u"\u56fe\u7247", None))
        self.video_view_button.setText(QCoreApplication.translate("yolo_detect", u"\u89c6\u9891", None))
        self.Model_view_button.setText(QCoreApplication.translate("yolo_detect", u"\u6a21\u578b", None))
        self.image_label.setText(QCoreApplication.translate("yolo_detect", u"TextLabel", None))
    # retranslateUi

