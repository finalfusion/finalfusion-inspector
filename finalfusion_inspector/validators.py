from enum import Enum

from PyQt5.QtGui import QValidator


class WordStatus(Enum):
    KNOWN = 0
    SUBWORD = 1
    UNKNOWN = 2


def applyValidityColor(sender):
    if not sender.hasAcceptableInput():
        style = "background-color: salmon"
    else:
        validator = sender.validator()
        if validator.word_status(sender.text()) == WordStatus.SUBWORD:
            style = "background-color: yellow"
        else:
            style = ""

    sender.setStyleSheet(style)


def is_vocab_word(model, word):
    vocab = model.embeddings.vocab()

    indices = vocab.get(word)
    if indices is None:
        return WordStatus.UNKNOWN
    elif isinstance(indices, int):
        return WordStatus.KNOWN

    return WordStatus.SUBWORD


class QueryValidator(QValidator):
    def __init__(self, model):
        super(QueryValidator, self).__init__()
        self._model = model
        self.model.changed.connect(self.modelChanged)

    def modelChanged(self):
        self.changed.emit()

    def word_status(self, input_):
        return is_vocab_word(self.model, input_)

    def validate(self, input_, pos):
        wordStatus = is_vocab_word(self.model, input_)

        if wordStatus == WordStatus.KNOWN:
            return (QValidator.Acceptable, input_, pos)
        elif wordStatus == WordStatus.SUBWORD:
            return (QValidator.Acceptable, input_, pos)
        else:
            return (QValidator.Intermediate, input_, pos)

    @property
    def model(self):
        return self._model
