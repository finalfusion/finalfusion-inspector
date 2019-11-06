from PyQt5.QtCore import QAbstractItemModel, QVariant, Qt
from PyQt5.QtWidgets import QHeaderView, QWidget


from ui_similaritywidget import Ui_SimilarityWidget


class SimilarityModel(QAbstractItemModel):
    def __init__(self, embeddings):
        super(SimilarityModel, self).__init__()

        self._embeddings = embeddings
        self._similarities = []

    def clear(self):
        self._similarities = []
        self.layoutChanged.emit()

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if role == Qt.DisplayRole:
            wordSimilarity = self.similarities[index.row()]

            if index.column() == 0:
                return wordSimilarity.word
            elif index.column() == 1:
                return "%.4f" % wordSimilarity.similarity

    @property
    def embeddings(self):
        return self._embeddings

    def headerData(self, column, orientation, role):
        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            return QVariant()

        if column == 0:
            return "Word"
        elif column == 1:
            return "Cosine similarity"
        else:
            return QVariant()

    def index(self, row, column, parent):
        return self.createIndex(row, column)

    def rowCount(self, index):
        return len(self.similarities)

    @property
    def similarities(self):
        return self._similarities

    def query(self, word):
        self._similarities = self.embeddings.word_similarity(word, limit=20)
        self.layoutChanged.emit()


class SimilarityWidget(QWidget):
    def __init__(self, embeddings, statusBar):
        super(SimilarityWidget, self).__init__()

        self.ui = Ui_SimilarityWidget()
        self.ui.setupUi(self)

        self._embeddings = embeddings
        self._statusBar = statusBar

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
            self._statusBar.showMessage(
                "%s is out of the vocabulary and a subword lookup was not possible" %
                word)
            return
        elif indices[0] < len(self._embeddings.vocab()):
            self._statusBar.showMessage("%s is in the vocabulary" % word)
        else:
            self._statusBar.showMessage("%s is out of vocabulary" % word)

        self.similarityModel.query(word)

    @property
    def similarityModel(self):
        return self._similarityModel
