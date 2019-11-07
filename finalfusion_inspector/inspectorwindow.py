import finalfusion
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow

from finalfusion_inspector.ui_inspectorwindow import Ui_InspectorWindow
from finalfusion_inspector.similarity import AnalogyWidget, SimilarityModel, SimilarityWidget


class InspectorWindow(QMainWindow):
    def __init__(self, embeddings):
        super(InspectorWindow, self).__init__()

        self.ui = Ui_InspectorWindow()
        self.ui.setupUi(self)

        self._tabWidgets = [SimilarityWidget(SimilarityModel(embeddings)), AnalogyWidget(SimilarityModel(embeddings))]

        self.ui.tabWidget.addTab(
            self.tabWidgets[0],
            "Similarity")

        self.ui.tabWidget.addTab(
            self.tabWidgets[1],
            "Analogy")

        self.ui.openAction.triggered.connect(self.openEmbeddings)

    @property
    def tabWidgets(self):
        return self._tabWidgets

    def openEmbeddings(self):
        embeddingsFile, _ = QFileDialog.getOpenFileName(self,
            caption="Open embeddings file", filter="Finalfusion Embeddings (*.fifu)")

        # If the user clicker 'Cancel', do nothing.
        if embeddingsFile == '':
            return

        # Try to read the embeddings.
        try:
            embeddings = finalfusion.Embeddings(embeddingsFile, mmap=True)
        except Exception as e:
            QMessageBox.critical(
                self, "Cannot load embeddings", "Cannot load embeddings from %s: %s" %
                (embeddingsFile, e))

            # Keep the existing embeddings open.
            return

        # Switch to the newly-loaded embeddings.
        for widget in self.tabWidgets:
            widget.model.switchEmbeddings(embeddings)
