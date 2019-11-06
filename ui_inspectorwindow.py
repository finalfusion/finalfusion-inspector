# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_inspectorwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InspectorWindow(object):
    def setupUi(self, InspectorWindow):
        InspectorWindow.setObjectName("InspectorWindow")
        InspectorWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(InspectorWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.queryLineEdit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queryLineEdit.sizePolicy().hasHeightForWidth())
        self.queryLineEdit.setSizePolicy(sizePolicy)
        self.queryLineEdit.setObjectName("queryLineEdit")
        self.horizontalLayout.addWidget(self.queryLineEdit)
        self.queryPushButton = QtWidgets.QPushButton(self.groupBox)
        self.queryPushButton.setObjectName("queryPushButton")
        self.horizontalLayout.addWidget(self.queryPushButton)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.similarListView = QtWidgets.QListView(self.groupBox_2)
        self.similarListView.setObjectName("similarListView")
        self.verticalLayout_2.addWidget(self.similarListView)
        self.verticalLayout.addWidget(self.groupBox_2)
        InspectorWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(InspectorWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        InspectorWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(InspectorWindow)
        self.statusbar.setObjectName("statusbar")
        InspectorWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(InspectorWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(InspectorWindow)
        self.actionQuit.triggered.connect(InspectorWindow.close)
        QtCore.QMetaObject.connectSlotsByName(InspectorWindow)

    def retranslateUi(self, InspectorWindow):
        _translate = QtCore.QCoreApplication.translate
        InspectorWindow.setWindowTitle(_translate("InspectorWindow", "finalfusion inspector"))
        self.groupBox.setTitle(_translate("InspectorWindow", "Query"))
        self.queryPushButton.setText(_translate("InspectorWindow", "Find similar words"))
        self.groupBox_2.setTitle(_translate("InspectorWindow", "Results"))
        self.menuFile.setTitle(_translate("InspectorWindow", "File"))
        self.actionQuit.setText(_translate("InspectorWindow", "&Quit"))
