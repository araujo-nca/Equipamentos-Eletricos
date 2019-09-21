# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile


class interface:
    def __init__(self):
        pass  # call __init__(self) of the custom base class here


    if __name__ == "__main__":
        app = QApplication(sys.argv)

        ui_file = QFile("Equipamentos.ui")
        ui_file.open(QFile.ReadOnly)

        loader = QUiLoader()
        window = loader.load(ui_file)
        ui_file.close()
        window.show()

        sys.exit(app.exec_())
