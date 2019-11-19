import math
import platform


from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QThreadPool, QVariant, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QHeaderView, QStyleOptionProgressBar, QStyle, QStyledItemDelegate, QWidget


from finalfusion_inspector.ui_analogywidget import Ui_AnalogyWidget
from finalfusion_inspector.ui_similaritywidget import Ui_SimilarityWidget
from finalfusion_inspector.util import RunnableFunction
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
        self.ui.similarView.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents)

        # Does not work correctly on macOS, see:
        # https://bugreports.qt.io/browse/QTBUG-72558
        if platform.system() != "Darwin":
            self.ui.similarView.setItemDelegateForColumn(
                1, SimilarityCellDelegate())

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
        pool = QThreadPool.globalInstance()
        runnable = RunnableFunction(self.embeddings.analogy,
                                    words[0], words[1], words[2], limit=20)
        runnable.signals.success.connect(self.processResults)
        pool.start(runnable)

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

    def processResults(self, results):
        self._similarities = results
        self.layoutChanged.emit()

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
        pool = QThreadPool.globalInstance()
        runnable = RunnableFunction(self.embeddings.word_similarity, word, limit=20)
        runnable.signals.success.connect(self.processResults)
        pool.start(runnable)


class SimilarityCellDelegate(QStyledItemDelegate):
    def __init__(self):
        super(SimilarityCellDelegate, self).__init__()

    def angularSimilarity(self, cosineSimilarity):
        return 1.0 - (math.acos(cosineSimilarity) / math.pi)

    def paint(self, painter, option, index):
        angularSimilarity = self.angularSimilarity(float(index.data()))

        progressBarOption = QStyleOptionProgressBar()
        progressBarOption.rect = option.rect
        progressBarOption.minimum = 0
        progressBarOption.maximum = 100
        progressBarOption.progress = round(100.0 * angularSimilarity)
        progressBarOption.text = "%.2f" % angularSimilarity
        progressBarOption.textVisible = True

        QApplication.style().drawControl(
            QStyle.CE_ProgressBar, progressBarOption, painter)


class SimilarityWidget(QWidget):
    def __init__(self, model):
        super(SimilarityWidget, self).__init__()

        self._model = model

        self.ui = Ui_SimilarityWidget()
        self.ui.setupUi(self)

        self.ui.similarView.setModel(self.model)
        self.ui.similarView.horizontalHeader() \
                           .setSectionResizeMode(QHeaderView.Stretch)
        if platform.system() != "Darwin":
            self.ui.similarView.setItemDelegateForColumn(
                1, SimilarityCellDelegate())
        self.ui.similarView.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents)

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
