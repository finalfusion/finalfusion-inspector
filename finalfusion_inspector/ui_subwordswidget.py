# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_subwordswidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SubwordsWidget(object):
    def setupUi(self, SubwordsWidget):
        SubwordsWidget.setObjectName("SubwordsWidget")
        SubwordsWidget.resize(731, 570)
        self.verticalLayout = QtWidgets.QVBoxLayout(SubwordsWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(SubwordsWidget)
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
        self.groupBox_2 = QtWidgets.QGroupBox(SubwordsWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.subwordsView = QtWidgets.QTableView(self.groupBox_2)
        self.subwordsView.setAlternatingRowColors(True)
        self.subwordsView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.subwordsView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.subwordsView.setSortingEnabled(True)
        self.subwordsView.setObjectName("subwordsView")
        self.verticalLayout_2.addWidget(self.subwordsView)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(SubwordsWidget)
        QtCore.QMetaObject.connectSlotsByName(SubwordsWidget)

    def retranslateUi(self, SubwordsWidget):
        _translate = QtCore.QCoreApplication.translate
        SubwordsWidget.setWindowTitle(_translate("SubwordsWidget", "Form"))
        self.groupBox.setTitle(_translate("SubwordsWidget", "Query"))
        self.queryPushButton.setText(_translate("SubwordsWidget", "Subwords"))
        self.groupBox_2.setTitle(_translate("SubwordsWidget", "Results"))
