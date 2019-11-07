#!/usr/bin/env python3

import argparse
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
import finalfusion

from finalfusion_inspector.inspectorwindow import InspectorWindow


parser = argparse.ArgumentParser(description='Inspect finalfusion embeddings.')
parser.add_argument(
    'embeddings',
    metavar='EMBEDS',
    nargs='?',
    help='the embeddings to inspect')


def openEmbeddingsDialog():
    embeddingsFile, _ = QFileDialog.getOpenFileName(
        caption="Open embeddings file", filter="Finalfusion Embeddings (*.fifu)")
    if embeddingsFile == '':
        print("No filename selected", file=sys.stderr)
        sys.exit(1)

    return embeddingsFile


def main():
    args = parser.parse_args()

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    embeddingsFile = args.embeddings
    if embeddingsFile is None:
        embeddingsFile = openEmbeddingsDialog()

    try:
        embeddings = finalfusion.Embeddings(embeddingsFile, mmap=True)
    except Exception as e:
        QMessageBox.critical(
            None, "Cannot load embeddings", "Cannot load embeddings from %s: %s" %
            (embeddingsFile, e))
        sys.exit(1)

    window = InspectorWindow(embeddings)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
