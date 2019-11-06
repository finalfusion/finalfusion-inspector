# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_analogywidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AnalogyWidget(object):
    def setupUi(self, AnalogyWidget):
        AnalogyWidget.setObjectName("AnalogyWidget")
        AnalogyWidget.resize(731, 570)
        self.verticalLayout = QtWidgets.QVBoxLayout(AnalogyWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(AnalogyWidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.analogy1Edit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.analogy1Edit.sizePolicy().hasHeightForWidth())
        self.analogy1Edit.setSizePolicy(sizePolicy)
        self.analogy1Edit.setObjectName("analogy1Edit")
        self.horizontalLayout.addWidget(self.analogy1Edit)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.analogy2Edit = QtWidgets.QLineEdit(self.groupBox)
        self.analogy2Edit.setObjectName("analogy2Edit")
        self.horizontalLayout.addWidget(self.analogy2Edit)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.analogy3Edit = QtWidgets.QLineEdit(self.groupBox)
        self.analogy3Edit.setObjectName("analogy3Edit")
        self.horizontalLayout.addWidget(self.analogy3Edit)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.queryPushButton = QtWidgets.QPushButton(self.groupBox)
        self.queryPushButton.setObjectName("queryPushButton")
        self.horizontalLayout.addWidget(self.queryPushButton)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(AnalogyWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.similarView = QtWidgets.QTableView(self.groupBox_2)
        self.similarView.setAlternatingRowColors(True)
        self.similarView.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.similarView.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self.similarView.setObjectName("similarView")
        self.verticalLayout_2.addWidget(self.similarView)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(AnalogyWidget)
        QtCore.QMetaObject.connectSlotsByName(AnalogyWidget)

    def retranslateUi(self, AnalogyWidget):
        _translate = QtCore.QCoreApplication.translate
        AnalogyWidget.setWindowTitle(_translate("AnalogyWidget", "Form"))
        self.groupBox.setTitle(_translate("AnalogyWidget", "Query"))
        self.label.setText(_translate("AnalogyWidget", "is to"))
        self.label_2.setText(_translate("AnalogyWidget", "as"))
        self.label_3.setText(_translate("AnalogyWidget", "is to?"))
        self.queryPushButton.setText(
            _translate(
                "AnalogyWidget",
                "Find analogies"))
        self.groupBox_2.setTitle(_translate("AnalogyWidget", "Results"))
