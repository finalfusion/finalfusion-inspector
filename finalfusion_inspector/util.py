from PyQt5.QtCore import QObject, QRunnable, pyqtSignal


class RunnableFunctionSignals(QObject):
    error = pyqtSignal(Exception)
    success = pyqtSignal(object)


class RunnableFunction(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(RunnableFunction, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = RunnableFunctionSignals()

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            self.signals.error.emit(e)
        else:
            self.signals.success.emit(result)
