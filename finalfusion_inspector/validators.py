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


class QueryValidator(QValidator):
    def __init__(self, vocab):
        super(QueryValidator, self).__init__()
        self._vocab = vocab

    def word_status(self, input_):
        return is_vocab_word(self.vocab, input_)

    def validate(self, input_, pos):
        wordStatus = is_vocab_word(self.vocab, input_)

        if wordStatus == WordStatus.KNOWN:
            return (QValidator.Acceptable, input_, pos)
        elif wordStatus == WordStatus.SUBWORD:
            return (QValidator.Acceptable, input_, pos)
        else:
            return (QValidator.Intermediate, input_, pos)

    @property
    def vocab(self):
        return self._vocab
