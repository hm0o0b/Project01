import cv2
import mediapipe as mp
import numpy as np
from detect_point_gesture import get_hand_type, get_finger_status, recognize_gesture
from show_selection_menu import *

#mediapipe설정
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands = 2,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)

#이미지 위치 시작좌표 가져오기
icon_positions = get_icon_positions()

def select_frame_w_point(frame):   
    h, w, _ = frame.shape
    icon_index = -1
    
    # 손 인식하기
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_results = hands.process(rgb_frame)
    
    if hand_results.multi_hand_landmarks:
        #왼오 검지 손끝 인식 & 화면 표시
        for hand_landmarks in hand_results.multi_hand_landmarks:
            hand_type = get_hand_type(hand_landmarks)
            finger_status = get_finger_status(hand_landmarks)
            gesture =  recognize_gesture(hand_type, finger_status)
            #print(hand_type, gesture)
            
            finger_tip = hand_landmarks.landmark[8]
            fx, fy = int(finger_tip.x *w), int(finger_tip.y * h)
            cv2.circle(frame, (fx, fy), 5, (255, 0, 255), -1)            
        
        for icon_index, (icon_x, icon_y) in enumerate(icon_positions.values()):            
                        
            #손가락 위치에 따른 선택 여부 판단            
            if icon_x <= fx <= icon_x + icon_width and icon_y <= fy <= icon_y + icon_height:
                
                if icon_index == 0:
                    print("첫번째 아이콘 선택")            
                elif icon_index == 1:
                    print("두번쨰 아이콘 선택")
                elif icon_index == 2:
                    print("세번째 아이콘 선택")
                elif icon_index == 3: 
                    print("네번째 아이콘 선택")
                # 현재 선택된 아이콘 인덱스를 반환 
                
                #print("1 = ", icon_index)   
                               
                return frame, icon_index  
            
    # 아이콘 이외 범위 (기본값)
    icon_index = -1
    return frame, icon_index 



    

