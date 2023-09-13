import cv2
import mediapipe as mp
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

class FaceMeshWidget(QWidget):
    def __init__(self):
        super().__init__()        
        self.layout = QVBoxLayout(self)
        self.video_label = QLabel(self)
        self.layout.addWidget(self.video_label)
        
        self.cap = cv2.VideoCapture(0)
        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)
        
    def update_frame(self):
        success, image = self.cap.read()
        if not success:
            return

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for id, lm in enumerate(face_landmarks.landmark):

                    if id in [4]: # simply check the ID
                        # print(lm)
                        ih, iw, ic = image.shape
                        x,y,z= int(lm.x*iw),int(lm.y*ih),int(lm.z*ic)
                        # print(id,x,y,z)
                        cv2.circle(image, (x, y), radius=3, color=(225, 0, 100), thickness=1)

                    if id in [13, 14]: # simply check the ID
                        # print(lm)
                        ih, iw, ic = image.shape
                        x,y,z= int(lm.x*iw),int(lm.y*ih),int(lm.z*ic)
                        # print(id,x,y,z)
                        cv2.circle(image, (x, y), radius=3, color=(0, 225, 100), thickness=1)

        h, w, ch = image.shape
        bytes_per_line = ch * w
        qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.video_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.cap.release()
        self.timer.stop()
        event.accept()