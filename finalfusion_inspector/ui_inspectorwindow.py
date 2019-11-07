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
        InspectorWindow.resize(600, 800)
        self.centralwidget = QtWidgets.QWidget(InspectorWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        InspectorWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(InspectorWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        InspectorWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(InspectorWindow)
        self.statusbar.setObjectName("statusbar")
        InspectorWindow.setStatusBar(self.statusbar)
        self.quitAction = QtWidgets.QAction(InspectorWindow)
        icon = QtGui.QIcon.fromTheme("application-exit")
        self.quitAction.setIcon(icon)
        self.quitAction.setObjectName("quitAction")
        self.openAction = QtWidgets.QAction(InspectorWindow)
        icon = QtGui.QIcon.fromTheme("document-open")
        self.openAction.setIcon(icon)
        self.openAction.setObjectName("openAction")
        self.menuFile.addAction(self.openAction)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.quitAction)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(InspectorWindow)
        self.tabWidget.setCurrentIndex(-1)
        self.quitAction.triggered.connect(InspectorWindow.close)
        QtCore.QMetaObject.connectSlotsByName(InspectorWindow)

    def retranslateUi(self, InspectorWindow):
        _translate = QtCore.QCoreApplication.translate
        InspectorWindow.setWindowTitle(_translate("InspectorWindow", "finalfusion inspector"))
        self.menuFile.setTitle(_translate("InspectorWindow", "&File"))
        self.quitAction.setText(_translate("InspectorWindow", "&Quit"))
        self.quitAction.setShortcut(_translate("InspectorWindow", "Ctrl+Q"))
        self.openAction.setText(_translate("InspectorWindow", "&Open embeddings…"))
        self.openAction.setShortcut(_translate("InspectorWindow", "Ctrl+O"))
