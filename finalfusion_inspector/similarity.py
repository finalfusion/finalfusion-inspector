from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QVariant, Qt, pyqtSignal
from PyQt5.QtWidgets import QHeaderView, QWidget


from finalfusion_inspector.ui_analogywidget import Ui_AnalogyWidget
from finalfusion_inspector.ui_similaritywidget import Ui_SimilarityWidget
from finalfusion_inspector.validators import QueryValidator, applyValidityColor


class AnalogyWidget(QWidget):
    def __init__(self, model):
        super(AnalogyWidget, self).__init__()

        self._model = model

        self.ui = Ui_AnalogyWidget()
        self.ui.setupUi(self)

        self.ui.similarView.setModel(self.model)
        self.ui.similarView.horizontalHeader() \
                           .setSectionResizeMode(QHeaderView.Stretch)

        self.ui.queryPushButton.setEnabled(False)
        self.ui.queryPushButton.clicked.connect(self.querySubmitted)

        self._edits = [
            self.ui.analogy1Edit,
            self.ui.analogy2Edit,
            self.ui.analogy3Edit]
        for edit in self._edits:
            edit.setValidator(QueryValidator(self.model))
            edit.textChanged.connect(self.applyValidityColor)
            edit.returnPressed.connect(self.querySubmitted)
            edit.textChanged.connect(self.queryChanged)

    def applyValidityColor(self):
        applyValidityColor(self.sender())

    def query(self):
        return list(map(lambda edit: edit.text(), self._edits))

    def queryChanged(self):
        allValid = all([edit.hasAcceptableInput() for edit in self._edits])
        self.ui.queryPushButton.setEnabled(allValid)

    def querySubmitted(self):
        # Should not be possible, but let's be paranoid.
        allValid = all([edit.hasAcceptableInput() for edit in self._edits])
        if not allValid:
            return

        self.model.clear()

        self.model.analogyQuery(self.query())

    @property
    def model(self):
        return self._model


class SimilarityModel(QAbstractItemModel):
    # This signal is emitted when the underlying embeddings have changed.
    changed = pyqtSignal()

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

    def parent(self, index):
        return QModelIndex()

    def rowCount(self, index):
        return len(self.similarities)

    def switchEmbeddings(self, embeddings):
        self._embeddings = embeddings
        self.clear()
        self.changed.emit()

    @property
    def similarities(self):
        return self._similarities

    def query(self, word):
        self._similarities = self.embeddings.word_similarity(word, limit=20)
        self.layoutChanged.emit()


class SimilarityWidget(QWidget):
    def __init__(self, model):
        super(SimilarityWidget, self).__init__()

        self._model = model

        self.ui = Ui_SimilarityWidget()
        self.ui.setupUi(self)

        self.ui.similarView.setModel(self.model)
        self.ui.similarView.horizontalHeader() \
                           .setSectionResizeMode(QHeaderView.Stretch)

        self.ui.queryPushButton.setEnabled(False)
        self.ui.queryPushButton.clicked.connect(self.querySubmitted)

        self.ui.queryLineEdit.setValidator(
            QueryValidator(self.model))
        self.ui.queryLineEdit.textChanged.connect(self.applyValidityColor)
        self.ui.queryLineEdit.returnPressed.connect(self.querySubmitted)
        self.ui.queryLineEdit.textChanged.connect(self.queryChanged)

    def applyValidityColor(self):
        applyValidityColor(self.sender())

    @property
    def query(self):
        return self.ui.queryLineEdit.text().strip()

    def queryChanged(self):
        self.ui.queryPushButton.setEnabled(
            self.ui.queryLineEdit.hasAcceptableInput())

    def querySubmitted(self):
        # Should not be possible, but let's be paranoid.
        if not self.ui.queryLineEdit.hasAcceptableInput():
            return

        self.model.clear()

        self.model.query(self.query)

    @property
    def model(self):
        return self._model
