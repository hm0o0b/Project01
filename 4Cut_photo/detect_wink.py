import cv2
import mediapipe as mp
import numpy as np
from add_heart_sticker import add_heart

##### MediaPipe 설정 #####
mp_face_mesh = mp.solutions.face_mesh #mp라이브러이의 face_mesh 모듈 가져옴, mp_face_mesh는 별칭
face_mesh = mp_face_mesh.FaceMesh( # FaceMesh클래스의 객체 face_mesh 설정
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5,
    refine_landmarks=True
)

# 윙크 인지 - 흰눈동자의 면적계산
def detect_wink(frame, face_results):    
    
    h, w, _ = frame.shape
    wink_case = False
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
    
            #흰자 랜드마크 
            left_sclera = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
            right_sclera = [362, 398, 384, 385, 386, 387, 388, 466, 263, 249, 390, 373, 374, 380, 381, 382]
            
            # 왼쪽 흰눈동자 좌표 리스트
            left_sclera_points = []
            for i in range(len(left_sclera)):
                p = left_sclera[i]
                x, y = int(face_landmarks.landmark[p].x * w), int(face_landmarks.landmark[p].y * h)
                left_sclera_points.append((x, y))
                
            # 왼쪽 흰눈동자 면적 계산
            left_sclera_area = cv2.contourArea(np.array(left_sclera_points))    
            
            # 오른쪽 흰눈동자 좌표 리스트
            right_sclera_points = []
            for i in range(len(right_sclera)):
                p = right_sclera[i]
                x, y = int(face_landmarks.landmark[p].x * w), int(face_landmarks.landmark[p].y * h)
                right_sclera_points.append((x, y))
            
            # 오른쪽 흰눈동자 면적 계산
            right_sclera_area = cv2.contourArea(np.array(right_sclera_points))
            
            wink_case = abs(left_sclera_area- right_sclera_area) >= 50   
                
            #wink_case에 속하면 바로 하트스티커 올리기기
            if wink_case :
                
                frame = add_heart(face_landmarks, frame, w, h)
              
                
    return frame, wink_case

