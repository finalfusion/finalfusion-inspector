from PyQt5.QtWidgets import QMainWindow

from finalfusion_inspector.ui_inspectorwindow import Ui_InspectorWindow
from finalfusion_inspector.similarity import AnalogyWidget, SimilarityModel, SimilarityWidget


class InspectorWindow(QMainWindow):
    def __init__(self, embeddings):
        super(InspectorWindow, self).__init__()

        self.ui = Ui_InspectorWindow()
        self.ui.setupUi(self)

        self.ui.tabWidget.addTab(
            SimilarityWidget(
                SimilarityModel(embeddings)),
            "Similarity")

        self.ui.tabWidget.addTab(
            AnalogyWidget(
                SimilarityModel(embeddings)),
            "Analogy")
