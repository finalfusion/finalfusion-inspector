from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QSortFilterProxyModel, QVariant, Qt, pyqtSignal
from PyQt5.QtWidgets import QHeaderView, QWidget
from finalfusion.vocab.subword import SubwordVocab


from finalfusion_inspector.ui_subwordswidget import Ui_SubwordsWidget
from finalfusion_inspector.validators import QueryValidator, applyValidityColor


class SubwordsModel(QAbstractItemModel):
    # This signal is emitted when the underlying embeddings have changed.
    changed = pyqtSignal()

    def __init__(self, embeddings):
        super(SubwordsModel, self).__init__()

        self._embeddings = embeddings
        self._subwords = []

    def clear(self):
        self._subwords = []
        self.layoutChanged.emit()

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if role == Qt.DisplayRole:
            ngram, ngram_index = self.subwords[index.row()]

            if index.column() == 0:
                return ngram
            elif index.column() == 1:
                return ngram_index
        elif role == Qt.TextAlignmentRole:
            if index.column() == 1:
                return Qt.AlignRight
            else:
                return QVariant()

    @property
    def embeddings(self):
        return self._embeddings

    def headerData(self, column, orientation, role):
        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            return QVariant()

        if column == 0:
            return "Word"
        elif column == 1:
            return "Index"
        else:
            return QVariant()

    def index(self, row, column, parent):
        return self.createIndex(row, column)

    def parent(self, index):
        return QModelIndex()

    def rowCount(self, index):
        return len(self.subwords)

    def switchEmbeddings(self, embeddings):
        self._embeddings = embeddings
        self.clear()
        self.changed.emit()

    @property
    def subwords(self):
        return self._subwords

    def query(self, word):
        if not isinstance(self.embeddings.vocab, SubwordVocab):
            self._subwords = []
        else:
            self._subwords = self.embeddings.vocab.subword_indexer.subword_indices(
                word, with_ngrams=True)

        self.layoutChanged.emit()


class SubwordsWidget(QWidget):
    def __init__(self, model):
        super(SubwordsWidget, self).__init__()

        self._model = model

        self.ui = Ui_SubwordsWidget()
        self.ui.setupUi(self)

        proxyModel = QSortFilterProxyModel(self)
        proxyModel.setSourceModel(self.model)
        self.ui.subwordsView.setModel(proxyModel)
        self.ui.subwordsView.horizontalHeader() \
                           .setSectionResizeMode(QHeaderView.Stretch)
        self.ui.subwordsView.sortByColumn(1, Qt.AscendingOrder)

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
