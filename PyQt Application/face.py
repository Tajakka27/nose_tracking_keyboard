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

        self.p_nose_x = self.p_nose_y = 0 
        self.p_lip = 0

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
                    ih, iw, ic = image.shape
                    if id == 4:                            
                        nose_x, nose_y = int(lm.x*iw),int(lm.y*ih)
                        cv2.circle(image, (nose_x, nose_y), radius=3, color=(225, 0, 100), thickness=1)
                    elif id == 13:
                        lip_u_x, lip_u_y = int(lm.x*iw),int(lm.y*ih)                     
                        cv2.circle(image, (lip_u_x, lip_u_y), radius=3, color=(0, 225, 100), thickness=1)
                    elif id == 14:
                        lip_d_x, lip_d_y = int(lm.x*iw),int(lm.y*ih)                     
                        cv2.circle(image, (lip_d_x, lip_d_y), radius=3, color=(0, 225, 100), thickness=1)
                
            if abs(lip_d_y-lip_u_y)+abs(lip_d_x-lip_u_x) > 4:
                if self.p_lip == 0:
                    print("Clicked", lip_d_x-lip_u_x, lip_d_y-lip_u_y)
                self.p_lip = 1
            else:
                self.p_lip = 0
                    

        h, w, ch = image.shape
        bytes_per_line = ch * w
        qt_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.video_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.cap.release()
        self.timer.stop()
        event.accept()