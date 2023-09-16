from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
import sys
from face import *



# The Main Frame class...
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("interface.ui", self)
        
        # Define Widgets...
        central_widget = self.centralwidget
        self.video_layout= self.findChild(QVBoxLayout, 'verticalLayout_3')
        self.start_video_button = self.findChild(QPushButton, 'startVideoButton')
        self.end_video_button = self.findChild(QPushButton, 'endVideoButton')
        self.calibrate_button = self.findChild(QPushButton, 'calibrateButton')
        
        # Edit widget UI...
        self.calibrate_button.hide()
        self.end_video_button.hide()
        
        # Button Controls
        self.start_video_button.clicked.connect(self.startVideo)
        self.end_video_button.clicked.connect(self.endVideo)
        self.calibrate_button.clicked.connect(self.calibrate)

    def startVideo(self):
        self.video = FaceMeshWidget()
        self.video_layout.addWidget(self.video)
        self.start_video_button.hide()
        self.calibrate_button.show()
        self.end_video_button.show()
        
    def calibrate(self):
        self.video.calibrate()
    
    def endVideo(self):        
        self.video.cap.release()
        self.video.timer.stop()
        
        self.video_layout.removeWidget(self.video)
        self.video.deleteLater()
        self.video = None
        
        self.start_video_button.show()
        self.calibrate_button.hide()
        self.end_video_button.hide()
        
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowIcon(QIcon('Images\logo.png'))
    window.show()
    app.exec()