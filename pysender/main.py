import sys

from PyQt5.QtWidgets import QApplication

from pysender.ui import MainWindow

if __name__ == "__main__":
    application = QApplication(sys.argv)
    main_window = MainWindow()

    sys.exit(application.exec_())
