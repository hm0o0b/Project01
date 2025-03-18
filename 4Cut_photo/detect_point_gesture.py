import cv2
import mediapipe as mp
import time
import numpy as np

## 포인트제스쳐 감지 & 보조개 위치에 검지손끝 위치 + 3초 유지 후 사진 촬영
# 손 인식 모듈 임포트, 오른손/왼손 구분은 중요하지 않,,,,however,.,
# 얼굴 인식 모듈 임포트 

#mediapipe 설정
mp_hands = mp.solutions.hands # MediaPipe의 손 인식 모듈인 hands를 mp_hands라는 별칭으로 임포트
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh #mp라이브러리의 /face_mesh모듈/을 가져옴, mp_face_mesh 별칭

# 객체 생성
hands = mp_hands.Hands( # MediaPipe에서 손 인식을 위한 Hands 클래스의 객체를 생성하는 코드
    max_num_hands = 2,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)
    
face_mesh = mp_face_mesh.FaceMesh() #FaceMesh클래스의 객체 face_mesh를 가져옴 

# 왼손, 오른손 구분                
def get_hand_type(hand_landmarks):
    if hand_landmarks.landmark[5].x < hand_landmarks.landmark[17].x:
        return "Right"
    else :
        return "Left"

# 손 제스처 구분
def recognize_gesture(hand_type, fingers_status):
    
    if hand_type == "Right": # 오른손일 경우
        if fingers_status == [0,0,0,0,0]:
            return 'fist'
        elif fingers_status == [0,1,0,0,0] or [1,1,0,0,0]:
            return 'point'
        elif fingers_status == [0,1,1,0,0]:
            return 'v'
        elif fingers_status == [1,1,1,1,1]:
            return 'hello'
        else: return 'None'
        #elif fingers_status == [0,0,0,0,0]:
        #return 'thumbsup'
        
    else : #왼손인 경우     
        if fingers_status == [1,0,0,0,0]:
            return 'fist'
        elif fingers_status == [1,1,0,0,0] or [0,1,0,0,0]:
            return 'point'
        elif fingers_status == [1,1,1,0,0]:
            return 'v'
        elif fingers_status == [0,1,1,1,1]:
            return 'hello'
        else: return 'None'

# 손가락 접힘/펼침 구분분        
def get_finger_status(hand_landmarks):    
    fingers = []   
    fingers.append(hand_landmarks.landmark[4].x < hand_landmarks.landmark[2].x)   # 엄지 (참-핌-1)          
    fingers.append(hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y)   # 검지 (참-핌-1)
    fingers.append(hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y) # 중지 (참-핌-1)
    fingers.append(hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y) # 약지 (참-핌-1)
    fingers.append(hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y) # 새끼 (참-핌-1)  
    return fingers

# 포인트 제스처 인식하기 (검지 손가락만 펼친 상태태)
def detect_point_gesture(frame, face_results, hand_results):
    h, w, _ = frame.shape
    point_case = False
    
    # 보조개 랜드마크, 보조개 좌표 초기값 설정
    left_dimple_index = 192  
    right_dimple_index = 416
    left_dimple_point = None
    right_dimple_point = None
    
    # 보조개 위치와 검지손가락 사이의 거리 초기값 설정
    left_distance = None
    right_distance = None
    
    #얼굴에 관한 설정 (보조개)
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            left_dimple_landmark = face_landmarks.landmark[left_dimple_index] #192 
            left_dimple_x, left_dimple_y = int(left_dimple_landmark.x * w), int(left_dimple_landmark.y * h) #화면상에 left_dimple좌표 
            
            right_dimple_landmark = face_landmarks.landmark[right_dimple_index] #416
            right_dimple_x, right_dimple_y = int(right_dimple_landmark.x * w), int(right_dimple_landmark.y * h) #화면상에 right_dimple좌표 
                  
            left_dimple_point = left_dimple_x, left_dimple_y 
            right_dimple_point = right_dimple_x, right_dimple_y
            
            cv2.circle(frame, left_dimple_point, 5, (0, 0, 255), -1) #빨간색
            cv2.circle(frame, right_dimple_point, 5, (0,255, 0), -1) #초록색

    #손(point)에 관한 설정
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            hand_type = get_hand_type(hand_landmarks)           
            fingers_status = get_finger_status(hand_landmarks)
            gesture = recognize_gesture(hand_type, fingers_status)
            print(hand_type, gesture)
            
            finger_tip = hand_landmarks.landmark[8]
            fx, fy = int(finger_tip.x * w), int(finger_tip.y * h)            
            cv2.circle(frame, (fx, fy), 5, (255, 0, 0), -1) #검지 끝 파란색으로 표시
            
            if left_dimple_point:
                left_distance = np.linalg.norm(np.array(left_dimple_point) - np.array((fx, fy)))
                if left_distance < 20:
                    print("왼쪽 볼터치 감지")
                    
            if right_dimple_point:
                right_distance = np.linalg.norm(np.array(right_dimple_point) - np.array((fx, fy)))
                if right_distance < 20:
                    print("오른쪽 볼터치 감지") 
            
            #볼콕 조건 - hand_gesture == point
            if gesture == 'point' and ((left_distance is not None and left_distance <20) or
                                       (right_distance is not None and right_distance <20)):
                point_case = True
            else :
                point_case = False 
                     
    return frame, point_case
                
            
   
        