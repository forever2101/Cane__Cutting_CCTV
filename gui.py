# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1200, 600)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox_setup = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_setup.setGeometry(QtCore.QRect(1000, 50, 170, 300))
        self.groupBox_setup.setObjectName("groupBox_setup")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_setup.setLayout(self.horizontalLayout)
        self.verticalLayout_1 = QtWidgets.QVBoxLayout()
        self.verticalLayout_1.setObjectName("viticalLayout_1")
        self.horizontalLayout.addLayout(self.verticalLayout_1)
        self.NO_1 = QtWidgets.QPushButton()
        self.NO_1.setObjectName("NO_1")
        self.verticalLayout_1.addWidget(self.NO_1)
        self.NO_2 = QtWidgets.QPushButton()
        self.NO_2.setObjectName("NO_2")
        self.verticalLayout_1.addWidget(self.NO_2)
        self.NO_3 = QtWidgets.QPushButton()
        self.NO_3.setObjectName("NO_3")
        self.verticalLayout_1.addWidget(self.NO_3)
        self.label_image = QtWidgets.QLabel(self.centralwidget)
        self.label_image.setGeometry(QtCore.QRect(30, 30, 960, 540))
        self.label_image.setStyleSheet("background-color: rgb(233, 185, 110);")
        self.label_image.setText("")
        self.label_image.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image.setObjectName("label_image")
        self.widget = QtWidgets.QWidget(self.centralwidget)######
        self.widget.setGeometry(QtCore.QRect(1030, 400, 120, 140)) #####
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_openVideo = QtWidgets.QPushButton(self.widget)
        self.pushButton_openVideo.setObjectName("pushButton_openVideo")
        self.verticalLayout.addWidget(self.pushButton_openVideo)
        self.pushButton_start = QtWidgets.QPushButton(self.widget)
        self.pushButton_start.setObjectName("pushButton_start")
        self.verticalLayout.addWidget(self.pushButton_start)
        mainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "CANE_CUTTING_CCTV"))
        self.groupBox_setup.setTitle(_translate("mainWindow", "Detection Area Setup"))
        self.NO_1.setText(_translate("mainWindow", "NO_1"))
        self.NO_2.setText(_translate("mainWindow", "NO_2"))
        self.NO_3.setText(_translate("mainWindow", "NO_3"))
        self.pushButton_openVideo.setText(_translate("mainWindow", "Open Video"))
        self.pushButton_start.setText(_translate("mainWindow", "Start"))
