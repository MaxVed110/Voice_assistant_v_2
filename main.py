from core import Assistant
from PyQt5 import QtWidgets

if __name__ == '__main__':
    App = QtWidgets.QApplication([])
    window = Assistant()
    window.show()
    App.exec()


