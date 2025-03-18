import cv2
import mediapipe as mp

# 손 제스처 인식하기 (왼/오른손 구분, 손가락 접힙/펼침 구분, 손가락 상태에 따른 제스처 구분)

# 손 찾기 
mp_hands = mp.solutions.hands

# 손 그리기
mp_drawing = mp.solutions.drawing_utils

# 손 찾기 세부 설정
hands = mp_hands.Hands(
    max_num_hands = 2,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)

# 오른손 왼손 판별
def get_hand_type(hand_landmarks):
    if hand_landmarks.landmark[5].x < hand_landmarks.landmark[17].x:
        return "Right"
    else :
        return "Left"
    
#손가락 접힘/펼침 확인, True=펼침, False=접음
def get_finger_status(hand_landmarks):    
    fingers = []   
    fingers.append(hand_landmarks.landmark[4].x < hand_landmarks.landmark[2].x)   # 엄지 (참-핌-1)          
    fingers.append(hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y)   # 검지 (참-핌-1)
    fingers.append(hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y) # 중지 (참-핌-1)
    fingers.append(hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y) # 약지 (참-핌-1)
    fingers.append(hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y) # 새끼 (참-핌-1)  
    return fingers
 
def recognize_gesture(hand_type, fingers_status):
    if hand_type == "Right": # 오른손일 경우
        if fingers_status == [0,0,0,0,0]:
            return 'fist'
        elif fingers_status == [0,1,0,0,0]:
            return 'point'
        elif fingers_status == [0,1,1,0,0]:
            return 'v'
        elif fingers_status == [1,1,1,1,1]:
            return 'hello'
        else: return 'None'
       
    else : #왼손인 경우      
        if fingers_status == [1,0,0,0,0]:
            return 'fist'
        elif fingers_status == [1,1,0,0,0]:
            return 'point'
        elif fingers_status == [1,1,1,0,0]:
            return 'v'
        elif fingers_status == [0,1,1,1,1]:
            return 'hello'
        else: return 'None'
     
    
def detect_v_gesture(frame, hand_results): 
    h, w, _ = frame.shape
    v_case = False        
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            hand_type = get_hand_type(hand_landmarks)
            fingers_status = get_finger_status(hand_landmarks)
            gesture = recognize_gesture(hand_type, fingers_status)
            
            #생략가능
            #print(hand_type, gesture)            
            #mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)                    
        
            if gesture == 'v':
                v_case = 'v'
            else:
                v_case = None
    return frame, v_case
