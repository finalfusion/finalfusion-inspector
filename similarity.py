from PyQt5.QtCore import QAbstractItemModel, QVariant, Qt


class SimilarityModel(QAbstractItemModel):
    def __init__(self, embeddings):
        super(SimilarityModel, self).__init__()

        self._embeddings = embeddings
        self._similarities = []

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
