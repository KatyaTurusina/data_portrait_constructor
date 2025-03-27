import sys
from PyQt6.QtWidgets import QApplication
from ui import CSVViewer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CSVViewer()
    viewer.show()
    sys.exit(app.exec())
