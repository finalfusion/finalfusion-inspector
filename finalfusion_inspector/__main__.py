#!/usr/bin/env python3

import argparse
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
import finalfusion

from finalfusion_inspector.inspectorwindow import InspectorWindow


parser = argparse.ArgumentParser(description='Inspect finalfusion embeddings.')
parser.add_argument(
    'embeddings',
    metavar='EMBEDS',
    help='the embeddings to inspect')


def main():
    args = parser.parse_args()

    try:
        embeddings = finalfusion.Embeddings(args.embeddings, mmap=True)
    except Exception as e:
        print("Cannot load embeddings from %s: %s" % (args.embeddings, e))
        sys.exit(1)

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    window = InspectorWindow(embeddings)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
