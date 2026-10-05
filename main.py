import os
os.environ["QT_QPA_PLATFORM"] = "xcb"

import sys

from PyQt6.QtWidgets import QApplication

from database.database import Database
from ui.main_window import MainWindow


def main():

    database = Database()
    database.initialize()

    app = QApplication(sys.argv)

    with open("ui/styles.qss", "r") as file:
        app.setStyleSheet(
            file.read()
        )

    window = MainWindow(database)
    window.show()
    
    sys.exit(
        app.exec()
    )

if __name__ == "__main__":
    main()
