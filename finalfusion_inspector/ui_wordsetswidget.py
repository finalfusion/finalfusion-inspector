# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_wordsetswidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WordSetsWidget(object):
    def setupUi(self, WordSetsWidget):
        WordSetsWidget.setObjectName("WordSetsWidget")
        WordSetsWidget.resize(538, 165)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(WordSetsWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setObjectName("mainLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.wordsTextEdit = QtWidgets.QPlainTextEdit(WordSetsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wordsTextEdit.sizePolicy().hasHeightForWidth())
        self.wordsTextEdit.setSizePolicy(sizePolicy)
        self.wordsTextEdit.setTabChangesFocus(True)
        self.wordsTextEdit.setObjectName("wordsTextEdit")
        self.horizontalLayout.addWidget(self.wordsTextEdit)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(WordSetsWidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.twoDimRadio = QtWidgets.QRadioButton(self.groupBox)
        self.twoDimRadio.setChecked(True)
        self.twoDimRadio.setObjectName("twoDimRadio")
        self.verticalLayout.addWidget(self.twoDimRadio)
        self.threeDimRadio = QtWidgets.QRadioButton(self.groupBox)
        self.threeDimRadio.setObjectName("threeDimRadio")
        self.verticalLayout.addWidget(self.threeDimRadio)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.visualizeButton = QtWidgets.QPushButton(WordSetsWidget)
        self.visualizeButton.setObjectName("visualizeButton")
        self.verticalLayout_2.addWidget(self.visualizeButton)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.mainLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.mainLayout)

        self.retranslateUi(WordSetsWidget)
        QtCore.QMetaObject.connectSlotsByName(WordSetsWidget)

    def retranslateUi(self, WordSetsWidget):
        _translate = QtCore.QCoreApplication.translate
        WordSetsWidget.setWindowTitle(_translate("WordSetsWidget", "Form"))
        self.groupBox.setTitle(_translate("WordSetsWidget", "Dimensionality"))
        self.twoDimRadio.setText(_translate("WordSetsWidget", "2D"))
        self.threeDimRadio.setText(_translate("WordSetsWidget", "3D"))
        self.visualizeButton.setText(_translate("WordSetsWidget", "Compare"))
