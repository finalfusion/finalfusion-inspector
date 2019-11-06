from PyQt5.QtWidgets import QMainWindow

from ui_inspectorwindow import Ui_InspectorWindow

class InspectorWindow(QMainWindow):
    def __init__(self):
        super(InspectorWindow, self).__init__()

        self.ui = Ui_InspectorWindow()
        self.ui.setupUi(self)


