from matplotlib.backends.backend_qt5agg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget
from sklearn.manifold import MDS


from finalfusion_inspector.ui_wordsetswidget import Ui_WordSetsWidget
from finalfusion_inspector.validators import WordStatus, is_vocab_word


class MDSModel(QObject):
    changed = pyqtSignal(object, object)
    cleared = pyqtSignal()

    def __init__(self, embeddings, max_iter=2000, epsilon=1e-9):
        super(MDSModel, self).__init__()

        self._embeddings = embeddings
        self._coordinates = [[]]

        self._max_iter = max_iter
        self._epsilon = epsilon

    @property
    def embeddings(self):
        return self._embeddings

    @property
    def epsilon(self):
        return self._epsilon

    @property
    def coordinates(self):
        return self._coordinates

    def isValidQuery(self, words):
        queryWords = self.queryWords(words)
        return len(queryWords) > 1, queryWords

    @property
    def max_iter(self):
        return self._max_iter

    def queryWords(self, words):
        return list({word for word in words if is_vocab_word(
            self, word) != WordStatus.UNKNOWN})

    def switchEmbeddings(self, embeddings):
        self._embeddings = embeddings
        self._coordinates = [[]]
        self.cleared.emit()

    def update(self, words):
        isValid, words = self.isValidQuery(words)
        if not isValid:
            return

        vecs = [self.embeddings.embedding(word) for word in words]
        mds = MDS(
            n_components=2,
            dissimilarity="euclidean",
            max_iter=self.max_iter,
            eps=self.epsilon,
            random_state=42)
        self._coordinates = mds.fit_transform(vecs)
        self.changed.emit(words, self.coordinates)


class WordSetsWidget(QWidget):
    def __init__(self, model):
        super(WordSetsWidget, self).__init__()

        self._model = model

        self.ui = Ui_WordSetsWidget()
        self.ui.setupUi(self)

        self._canvas = canvas = FigureCanvas(Figure(figsize=(5, 5)))
        self.ui.verticalLayout.addWidget(canvas)
        self.ui.verticalLayout.addWidget(NavigationToolbar(canvas, self))
        self._subplot = self._canvas.figure.subplots()
        self._canvas.figure.tight_layout()

        self.model.changed.connect(self.visualizeWords)
        self.model.cleared.connect(self.clear)

        self.ui.wordsTextEdit.textChanged.connect(self.queryChanged)
        self.ui.visualizeButton.setEnabled(False)
        self.ui.visualizeButton.clicked.connect(self.updateQuery)

    def clear(self):
        self.subplot.clear()
        self.subplot.figure.canvas.draw()

    def isValidInput(self):
        words = self.query()
        isValid, _ = self.model.isValidQuery(words)
        return isValid

    def query(self):
        return self.ui.wordsTextEdit.toPlainText().strip().split()

    def queryChanged(self):
        self.ui.visualizeButton.setEnabled(self.isValidInput())

    def updateQuery(self):
        self.model.update(self.query())

    def visualizeWords(self, words, coords):
        self.subplot.clear()

        self.subplot.scatter(coords[:, 0], coords[:, 1])
        for i, word in enumerate(words):
            self.subplot.annotate(word, coords[i])

        self.subplot.figure.canvas.draw()

    @property
    def model(self):
        return self._model

    @property
    def subplot(self):
        return self._subplot