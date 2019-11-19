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
        WordSetsWidget.resize(402, 301)
        self.verticalLayout = QtWidgets.QVBoxLayout(WordSetsWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.wordsTextEdit = QtWidgets.QPlainTextEdit(WordSetsWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.wordsTextEdit.sizePolicy().hasHeightForWidth())
        self.wordsTextEdit.setSizePolicy(sizePolicy)
        self.wordsTextEdit.setTabChangesFocus(True)
        self.wordsTextEdit.setObjectName("wordsTextEdit")
        self.horizontalLayout.addWidget(self.wordsTextEdit)
        self.visualizeButton = QtWidgets.QPushButton(WordSetsWidget)
        self.visualizeButton.setObjectName("visualizeButton")
        self.horizontalLayout.addWidget(self.visualizeButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(WordSetsWidget)
        QtCore.QMetaObject.connectSlotsByName(WordSetsWidget)

    def retranslateUi(self, WordSetsWidget):
        _translate = QtCore.QCoreApplication.translate
        WordSetsWidget.setWindowTitle(_translate("WordSetsWidget", "Form"))
        self.visualizeButton.setText(_translate("WordSetsWidget", "Compare"))
