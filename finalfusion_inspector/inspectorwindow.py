import finalfusion
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QMainWindow

from finalfusion_inspector.ui_inspectorwindow import Ui_InspectorWindow
from finalfusion_inspector.metadata import MetadataDialog, MetadataModel
from finalfusion_inspector.word_sets import MDSModel, WordSetsWidget
from finalfusion_inspector.similarity import AnalogyWidget, SimilarityModel, SimilarityWidget
from finalfusion_inspector.subwords import SubwordsModel, SubwordsWidget


class InspectorWindow(QMainWindow):
    def __init__(self, embeddings):
        super(InspectorWindow, self).__init__()

        self.ui = Ui_InspectorWindow()
        self.ui.setupUi(self)

        self.ui.statusbar.hide()

        self._modelBackedWidgets = [
            SimilarityWidget(SimilarityModel(embeddings)), AnalogyWidget(SimilarityModel(embeddings)),
            SubwordsWidget(SubwordsModel(embeddings)), WordSetsWidget(MDSModel(embeddings))]

        self.ui.tabWidget.addTab(
            self.modelBackedWidgets[0],
            "Similarity")

        self.ui.tabWidget.addTab(
            self.modelBackedWidgets[1],
            "Analogy")

        self.ui.tabWidget.addTab(
            self.modelBackedWidgets[2],
            "Subwords")

        self.ui.tabWidget.addTab(
            self.modelBackedWidgets[3],
            "Word sets")

        self._metadataDialog = MetadataDialog(MetadataModel(embeddings))
        self._modelBackedWidgets.append(self._metadataDialog)

        self.ui.openAction.triggered.connect(self.openEmbeddings)
        self.ui.metadataAction.triggered.connect(self.showMetadata)

    @property
    def modelBackedWidgets(self):
        return self._modelBackedWidgets

    def openEmbeddings(self):
        embeddingsFile, _ = QFileDialog.getOpenFileName(self,
            caption="Open embeddings file", filter="Finalfusion Embeddings (*.fifu)")

        # If the user clicker 'Cancel', do nothing.
        if embeddingsFile == '':
            return

        # Try to read the embeddings.
        try:
            embeddings = finalfusion.load_finalfusion(embeddingsFile, mmap=True)
        except Exception as e:
            QMessageBox.critical(
                self, "Cannot load embeddings", "Cannot load embeddings from %s: %s" %
                (embeddingsFile, e))

            # Keep the existing embeddings open.
            return

        # Switch to the newly-loaded embeddings.
        for widget in self.modelBackedWidgets:
            widget.model.switchEmbeddings(embeddings)

    def showMetadata(self):
        self._metadataDialog.exec_()
