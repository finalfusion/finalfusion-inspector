from PyQt5.QtWidgets import QHeaderView, QMainWindow

from ui_inspectorwindow import Ui_InspectorWindow
from similarity import SimilarityModel


class InspectorWindow(QMainWindow):
    def __init__(self, embeddings):
        super(InspectorWindow, self).__init__()

        self.ui = Ui_InspectorWindow()
        self.ui.setupUi(self)

        self._embeddings = embeddings

        self._similarityModel = SimilarityModel(self._embeddings)

        self.ui.similarView.setModel(self.similarityModel)
        self.ui.similarView.horizontalHeader() \
                           .setSectionResizeMode(QHeaderView.Stretch)

        self.ui.queryPushButton.setEnabled(False)
        self.ui.queryPushButton.clicked.connect(self.querySubmitted)

        self.ui.queryLineEdit.returnPressed.connect(self.querySubmitted)
        self.ui.queryLineEdit.textChanged.connect(self.queryChanged)

    @property
    def query(self):
        return self.ui.queryLineEdit.text().strip()

    def queryChanged(self):
        self.ui.queryPushButton.setEnabled(len(self.query) != 0)

    def querySubmitted(self):
        word = self.query
        if len(word) == 0:
            return

        self.similarityModel.clear()

        # Figure out whether the word is unknown. Checking whether
        # there are multiple indices is not good enough, since short
        # words may only have one n-gram. So we check if the first
        # index is in the range of the vocab.
        indices = self._embeddings.vocab().item_to_indices(word)
        if indices is None or len(indices) == 0:
            self.statusBar().showMessage("%s is out of the vocabulary and a subword lookup was not possible" % word)
            return
        elif indices[0] < len(self._embeddings.vocab()):
            self.statusBar().showMessage("%s is in the vocabulary" % word)
        else:
            self.statusBar().showMessage("%s is out of vocabulary" % word)

        self.similarityModel.query(word)

    @property
    def similarityModel(self):
        return self._similarityModel
