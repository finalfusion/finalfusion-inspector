# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_metadatadialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MetadataDialog(object):
    def setupUi(self, MetadataDialog):
        MetadataDialog.setObjectName("MetadataDialog")
        MetadataDialog.resize(600, 400)
        self.verticalLayout = QtWidgets.QVBoxLayout(MetadataDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.metadataView = QtWidgets.QTableView(MetadataDialog)
        self.metadataView.setObjectName("metadataView")
        self.verticalLayout.addWidget(self.metadataView)
        self.buttonBox = QtWidgets.QDialogButtonBox(MetadataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MetadataDialog)
        self.buttonBox.accepted.connect(MetadataDialog.accept)
        self.buttonBox.rejected.connect(MetadataDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MetadataDialog)

    def retranslateUi(self, MetadataDialog):
        _translate = QtCore.QCoreApplication.translate
        MetadataDialog.setWindowTitle(
            _translate(
                "MetadataDialog",
                "Embeddings metadata"))
