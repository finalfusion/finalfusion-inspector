from enum import Enum


from PyQt5.QtCore import QAbstractItemModel, QVariant, Qt
from PyQt5.QtWidgets import QHeaderView, QWidget


from ui_analogywidget import Ui_AnalogyWidget
from ui_similaritywidget import Ui_SimilarityWidget


class WordStatus(Enum):
    KNOWN = 0
    SUBWORD = 1
    UNKNOWN = 2


def is_vocab_word(vocab, word):
    # Figure out whether the word is unknown. Checking whether
    # there are multiple indices is not good enough, since short
    # words may only have one n-gram. So we check if the first
    # index is in the range of the vocab.

    indices = vocab.item_to_indices(word)

    if indices is None or len(indices) == 0:
        return WordStatus.UNKNOWN
    elif indices[0] < len(vocab):
        return WordStatus.KNOWN

    return WordStatus.SUBWORD


class AnalogyWidget(QWidget):
    def __init__(self, embeddings, statusBar):
        super(AnalogyWidget, self).__init__()

        self.ui = Ui_AnalogyWidget()
        self.ui.setupUi(self)

        self._embeddings = embeddings
        self._statusBar = statusBar

        self._similarityModel = SimilarityModel(self._embeddings)

        self.ui.similarView.setModel(self.similarityModel)
        self.ui.similarView.horizontalHeader() \
                           .setSectionResizeMode(QHeaderView.Stretch)

        self.ui.queryPushButton.setEnabled(False)
        self.ui.queryPushButton.clicked.connect(self.querySubmitted)

        self.ui.analogy1Edit.returnPressed.connect(self.querySubmitted)
        self.ui.analogy2Edit.returnPressed.connect(self.querySubmitted)
        self.ui.analogy3Edit.returnPressed.connect(self.querySubmitted)
        self.ui.analogy1Edit.textChanged.connect(self.queryChanged)
        self.ui.analogy2Edit.textChanged.connect(self.queryChanged)
        self.ui.analogy3Edit.textChanged.connect(self.queryChanged)

    def query(self):
        return [
            self.ui.analogy1Edit.text().strip(),
            self.ui.analogy2Edit.text().strip(),
            self.ui.analogy3Edit.text().strip()]

    def is_query_empty(self):
        return any(len(q) == 0 for q in self.query())

    def queryChanged(self):
        self.ui.queryPushButton.setEnabled(not self.is_query_empty())

    def querySubmitted(self):
        if self.is_query_empty():
            return

        self.similarityModel.clear()

        query = self.query()

        query_status = [(q, is_vocab_word(self._embeddings.vocab(), q))
                        for q in query]
        query_unknowns = list(
            filter(
                lambda s: s[1] == WordStatus.UNKNOWN,
                query_status))
        if len(query_unknowns) != 0:
            self._statusBar.showMessage("Query that are not in the vocabulary: %s" % ", ".join(
                map(lambda q: q[0], query_unknowns)))
            return

        messageParts = []
        query_known = list(
            filter(
                lambda s: s[1] == WordStatus.KNOWN,
                query_status))
        print(list(map(lambda q: q[0], query_known)))
        if len(query_known) != 0:
            messageParts.append("In the vocabulary: %s" %
                                ", ".join(map(lambda q: q[0], query_known)))

        query_subword = list(
            filter(
                lambda s: s[1] == WordStatus.SUBWORD,
                query_status))
        print(query_subword)
        if len(query_subword) != 0:
            messageParts.append("In the subword vocabulary: %s" %
                                ", ".join(map(lambda q: q[0], query_subword)))

        self._statusBar.showMessage(", ".join(messageParts))

        self.similarityModel.analogyQuery(query)

    @property
    def similarityModel(self):
        return self._similarityModel


class SimilarityModel(QAbstractItemModel):
    def __init__(self, embeddings):
        super(SimilarityModel, self).__init__()

        self._embeddings = embeddings
        self._similarities = []

    def analogyQuery(self, words):
        self._similarities = self.embeddings.analogy(
            words[0], words[1], words[2], limit=20)
        self.layoutChanged.emit()

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

        wordStatus = is_vocab_word(self._embeddings.vocab(), word)
        if wordStatus == WordStatus.UNKNOWN:
            self._statusBar.showMessage(
                "%s is out of the vocabulary and a subword lookup was not possible" %
                word)
            return
        elif wordStatus == WordStatus.KNOWN:
            self._statusBar.showMessage("%s is in the vocabulary" % word)
        else:
            self._statusBar.showMessage(
                "%s is in the subword vocabulary" % word)

        self.similarityModel.query(word)

    @property
    def similarityModel(self):
        return self._similarityModel
