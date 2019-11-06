from PyQt5.QtWidgets import QMainWindow

from ui_inspectorwindow import Ui_InspectorWindow
from similarity import AnalogyWidget, SimilarityWidget


class InspectorWindow(QMainWindow):
    def __init__(self, embeddings):
        super(InspectorWindow, self).__init__()

        self.ui = Ui_InspectorWindow()
        self.ui.setupUi(self)

        self.ui.tabWidget.addTab(
            SimilarityWidget(
                embeddings,
                self.statusBar()),
            "Similarity")

        self.ui.tabWidget.addTab(
            AnalogyWidget(
                embeddings,
                self.statusBar()),
            "Analogy")
