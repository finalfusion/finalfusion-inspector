from PyQt5.QtCore import QAbstractItemModel, QModelIndex, QVariant, Qt
from PyQt5.QtWidgets import QHeaderView, QDialog


from finalfusion_inspector.ui_metadatadialog import Ui_MetadataDialog


class MetadataDialog(QDialog):
    def __init__(self, model):
        super(MetadataDialog, self).__init__()

        self._model = model

        self.ui = Ui_MetadataDialog()
        self.ui.setupUi(self)

        self.ui.metadataView.setModel(self.model)
        self.ui.metadataView.horizontalHeader() \
                            .setSectionResizeMode(QHeaderView.Stretch)

    @property
    def model(self):
        return self._model


class KeyValuePair:
    def __init__(self, key, value):
        self._key = key
        self._value = value

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value


class MetadataModel(QAbstractItemModel):
    def __init__(self, embeddings):
        super(MetadataModel, self).__init__()

        self._embeddings = embeddings
        self._metadata = []

        self.updateMetadata()

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        if role == Qt.DisplayRole:
            datum = self.metadata[index.row()]

            if index.column() == 0:
                return datum.key
            elif index.column() == 1:
                return datum.value

    @property
    def embeddings(self):
        return self._embeddings

    def headerData(self, column, orientation, role):
        if orientation != Qt.Horizontal or role != Qt.DisplayRole:
            return QVariant()

        if column == 0:
            return "Key"
        elif column == 1:
            return "Value"
        else:
            return QVariant()

    def index(self, row, column, parent):
        return self.createIndex(row, column)

    @property
    def metadata(self):
        return self._metadata

    def parent(self, index):
        return QModelIndex()

    def rowCount(self, index):
        return len(self.metadata)

    def switchEmbeddings(self, embeddings):
        self._embeddings = embeddings
        self.updateMetadata()

    def updateMetadata(self):
        self._metadata = []

        if not isinstance(self.embeddings.metadata, dict):
            self.layoutChanged.emit()
            return

        metadata = self.embeddings.metadata
        for key, value in metadata.items():
            if isinstance(value, float):
                value = "%.2e" % value
            else:
                value = str(value)
            self._metadata.append(KeyValuePair(key, value))

        self.layoutChanged.emit()
