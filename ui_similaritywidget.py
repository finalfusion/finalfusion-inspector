# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_similaritywidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SimilarityWidget(object):
    def setupUi(self, SimilarityWidget):
        SimilarityWidget.setObjectName("SimilarityWidget")
        SimilarityWidget.resize(731, 570)
        self.verticalLayout = QtWidgets.QVBoxLayout(SimilarityWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(SimilarityWidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.queryLineEdit = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.queryLineEdit.sizePolicy().hasHeightForWidth())
        self.queryLineEdit.setSizePolicy(sizePolicy)
        self.queryLineEdit.setObjectName("queryLineEdit")
        self.horizontalLayout.addWidget(self.queryLineEdit)
        self.queryPushButton = QtWidgets.QPushButton(self.groupBox)
        self.queryPushButton.setObjectName("queryPushButton")
        self.horizontalLayout.addWidget(self.queryPushButton)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(SimilarityWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.similarView = QtWidgets.QTableView(self.groupBox_2)
        self.similarView.setAlternatingRowColors(True)
        self.similarView.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.similarView.setObjectName("similarView")
        self.verticalLayout_2.addWidget(self.similarView)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(SimilarityWidget)
        QtCore.QMetaObject.connectSlotsByName(SimilarityWidget)

    def retranslateUi(self, SimilarityWidget):
        _translate = QtCore.QCoreApplication.translate
        SimilarityWidget.setWindowTitle(_translate("SimilarityWidget", "Form"))
        self.groupBox.setTitle(_translate("SimilarityWidget", "Query"))
        self.queryPushButton.setText(
            _translate(
                "SimilarityWidget",
                "Find similar words"))
        self.groupBox_2.setTitle(_translate("SimilarityWidget", "Results"))
