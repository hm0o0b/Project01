import cv2
import os
import mediapipe as mp
import time
import numpy as np
import gc
from detect_wink import detect_wink
from add_heart_sticker import add_heart
from detect_v_gesture import detect_v_gesture
from detect_point_gesture import detect_point_gesture
from show_gray_time import *
from show_selection_menu import show_selection_text, show_selection_icon
from select_frame import select_frame_w_point
from add_frame import add_frame, countdown_selection
from cut_veritical import *

# MediaPipe 설정
mp_face_mesh = mp.solutions.face_mesh #mp라이브러이의 face_mesh 모듈 가져옴, mp_face_mesh는 별칭
face_mesh = mp_face_mesh.FaceMesh( # FaceMesh클래스의 객체 face_mesh 설정
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5,
    refine_landmarks=True
) 
mp_hands = mp.solutions.hands
hands = mp_hands.Hands( # Hands 클래스의 객체 hands 설정
    max_num_hands = 2,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)
mp_drawing = mp.solutions.drawing_utils

# 제스쳐감지, 지속시간, cap_stage, 카운트다운, 카메라 변수
detected = False
start_time = None
count_text = ""
cap_stage = 0
img_cv = None
icon_index = None
select_case = None

#현재 파일이 위치한 디렉토리 기준으로 경로설정하기
#base_dir = os.path.dirname(os.path.abspath(__file__))
resource_path = os.path.join(base_dir, 'resources', 'heart.png')
#print("resource_path경로:", resource_path)

# 스티커 이미지 로드 (PNG)
# heart = cv2.imread(os.path.join(resource_path, 'heart.png'), cv2.IMREAD_UNCHANGED)
# if heart is None:
#     print("🔴 스티커 이미지 로드 실패! 파일 경로를 확인하세요.")
#     exit()

#현재 스크립트 위치 기준 output 폴더 경로 
base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, 'output') 
 
    
# 카운트다운 & 사진찍기
def countdown_capture(frame, detected, cap_case, count_text, start_time):
    
    global cap_stage

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    if cap_case and not detected :                    
        detected = True
        start_time = time.time()
        print("행동 감지! 카운트다운 시작") 
    
    if detected : 
        if start_time is None:
            start_time = time.time()
        elapsed_time = time.time() - start_time     

        # 특정 행동 감지되면, 카운트다운 시작
        if elapsed_time < 1 :
            count_text = ""        
        elif elapsed_time < 1.8:
            count_text = "3"
        elif elapsed_time < 2.4 :
            count_text = "2"                       
        elif elapsed_time < 3.2 :
            count_text = "1"                       
        else:
            # output 폴더에 저장
            file_path = os.path.join(output_dir, f"captured_image{cap_stage+1}.jpg")
            # 📸 사진 저장 후 초기화
            cv2.imwrite(file_path, frame)
            print("📸 사진이 저장되었습니다!")
            detected = False
            start_time = None
            count_text = ""            
            cap_stage += 1
            time.sleep(1)
                                
    #윙크 감지 후 윙크 해당 범위 벗어났을 때            
    if not cap_case and detected :
        detected = False
        start_time = None
        count_text = ""   
    
    return frame, detected, count_text, cap_stage, start_time

##### 카메라 열기-확인 #####
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("카메라를 열 수 없습니다")
    exit()

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break        
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    h, w, _ = frame.shape  #print(f"현재 프레임 크기: {w}x{h}")
    face_results = face_mesh.process(rgb_frame)
    hand_results = hands.process(rgb_frame)
    
    if cap_stage == 0 : #윙크감지      
        frame, cap_case = detect_wink(frame, face_results)
        frame, detected, count_text, cap_stage, start_time = countdown_capture(frame, detected, cap_case, count_text, start_time)
            
    elif cap_stage == 1 : #브이제스쳐    
        frame, cap_case = detect_v_gesture(frame, hand_results)
        frame, detected, count_text, cap_stage, start_time = countdown_capture(frame, detected, cap_case, count_text, start_time)
                    
    elif cap_stage == 2 : #볼콕
        frame, cap_case = detect_point_gesture(frame, face_results, hand_results)
        frame, detected, count_text, cap_stage, start_time = countdown_capture(frame, detected, cap_case, count_text, start_time)
        #start_grayscale = None 
        
    elif cap_stage == 3: #흑백모드        
        frame = add_datetime(frame)
        frame, cap_case = show_grayscale(frame)
        frame, detected, count_text, cap_stage, start_time = countdown_capture(frame, detected, cap_case, count_text, start_time)
    
    elif cap_stage == 4: #프레임 선택하기
        frame, icon_index = select_frame_w_point(frame)        
        frame = show_selection_text(frame)
        frame, icon_index, select_case = show_selection_icon(frame, icon_index)        
        frame, icon_index, cap_stage = countdown_selection(frame, icon_index, select_case, cap_stage)
        
    elif cap_stage == 5: # 프레임 합치기 

        cut_vertical()        
        img_cv, icon_index = add_frame(icon_index, img_cv)

        cv2.imshow("Add frame with 4cuts", img_cv)    
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        cap_stage =0
        icon_index = None
        reset_start()
        
    cv2.putText(frame, count_text, (320, 240), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 5, cv2.LINE_AA)    
    cv2.imshow('Iam hungry', frame)
    
    if cv2.waitKey(1) == 27:            
        break
    
    del frame
    del face_results, hand_results
    
    gc.collect()
        
# 종료 처리
cap.release()
cv2.destroyAllWindows()
   