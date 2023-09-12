from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import sys



# The Main Frame class...
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("interface.ui", self)
        
        # Define Widgets...
        central_widget = self.centralwidget
        central_layout = self.verticalLayout
        
        # Edit widget UI...
        central_widget.setLayout(central_layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowIcon(QIcon('Images\logo.png'))
    window.show()
    app.exec()