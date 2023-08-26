from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
import sys
from ui_main import Ui_MainWindow


class EasySort(QMainWindow):
    def __init__(self):
        super(EasySort, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


def main():
    app = QApplication(sys.argv)
    window = EasySort()

    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
