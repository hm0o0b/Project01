import mediapipe as mp
import os
import numpy as np
import cv2

# MediaPipe 초기화
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils
mp_face_detection = mp.solutions.face_detection

base_dir = os.path.dirname(os.path.abspath(__file__))
resources_dir = os.path.join(base_dir, 'resources')

# 투명 PNG 스티커 합성 함수  -> 이미지가 화면 프레임 밖으로 벗어나도 오류 발생하지 않도록      
def overlay_image(bg, fg, x_offset, y_offset, angle=0):
    fg_h, fg_w = fg.shape[:2]
    bg_h, bg_w = bg.shape[:2]
    
    # 오버레이할 영역이 배경 이미지 내에만 있도록 설정
    if x_offset < 0:  # 왼쪽 경계 벗어날 때
        fg = fg[:, -x_offset:]
        x_offset = 0
    if y_offset < 0:  # 위쪽 경계 벗어날 때
        fg = fg[-y_offset:, :]
        y_offset = 0

    # 배경 이미지 크기보다 스티커 이미지가 클 경우 자르기
    if x_offset + fg_w > bg_w:
        fg = fg[:, :bg_w - x_offset]
    if y_offset + fg_h > bg_h:
        fg = fg[:bg_h - y_offset, :]

    fg_h, fg_w = fg.shape[:2]
    
    # 이미지 회전(사람 기울기에 따른 기울기)
    if angle != 0:
        M = cv2.getRotationMatrix2D((fg_w / 2, fg_h / 2), angle, 1)
        fg = cv2.warpAffine(fg, M, (fg_w, fg_h))

    fg_h, fg_w = fg.shape[:2]
    

    # 배경에 스티커 오버레이
    for c in range(3):  # RGB 채널에 대해 처리
        bg[y_offset:y_offset + fg_h, x_offset:x_offset + fg_w, c] = \
            bg[y_offset:y_offset + fg_h, x_offset:x_offset + fg_w, c] * (1 - fg[:, :, 3] / 255.0) + \
            fg[:, :, c] * (fg[:, :, 3] / 255.0)
    
    return bg

#print("resources_dir 경로:", resources_dir)

def add_heart(face_landmarks, frame, w, h):
    # 01. 스티커 이미지 로드 (PNG)
    heart = cv2.imread(os.path.join(resources_dir, 'heart.png'), cv2.IMREAD_UNCHANGED)
    if heart is None:
        print("🔴 스티커 이미지 로드 실패! 파일 경로를 확인하세요.")
        exit()
    
    #face_landmarks가 범위를 벗어날 때 overlay 실행x
    if face_landmarks is None:
        return frame
    
    # 02. 눈 아래 스티커 위치 인덱스
    left_heart_index = 227
    right_heart_index = 449
    
    # 03. 얼굴에 관한 설정
    ## 왼쪽 오른쪽 하트스티커 놓을 자리표시 (관자놀이 랜드마크 -> x,y 좌표로)
    left_heart_landmark = face_landmarks.landmark[left_heart_index] #227
    left_heart_x, left_heart_y = int(left_heart_landmark.x * w), int(left_heart_landmark.y * h)
    
    right_heart_landmark = face_landmarks.landmark[right_heart_index] #449
    right_heart_x, right_heart_y = int(right_heart_landmark.x * w), int(right_heart_landmark.y * h)
    
    left_heart_point = left_heart_x, left_heart_y
    right_heart_point = right_heart_x, right_heart_y 
    
    cv2.circle(frame, left_heart_point, 2, (0, 255, 0), -1) #왼쪽 초록색
    cv2.circle(frame, right_heart_point, 2, (0, 0, 255), -1) #오른쪽 빨간색              

    # 얼굴의 기울기 각도 계산 (눈 좌표를 기준으로)
    dx = right_heart_landmark.x - left_heart_landmark.x
    dy = right_heart_landmark.y - left_heart_landmark.y
    angle = np.degrees(np.arctan2(dy, dx))  # 라디안을 각도로 변환
    angle = -angle #flip 때문에 기울기도 반대로
    
    # 얼굴 크기 기반 스티커 크기 조정
    face_width = abs(face_landmarks.landmark[454].x - face_landmarks.landmark[234].x) * frame.shape[1]
    sticker_size_1 = int(face_width * 0.3)
    sticker_size_2 = int(face_width * 0.25)
    heart_resized01 = cv2.resize(heart, (sticker_size_1, sticker_size_1))
    heart_resized02 = cv2.resize(heart, (sticker_size_2, sticker_size_2))   
    
    # 스티커 화면 밖으로 나가지 않도록 범위 설정(좌표)
    # 스티커가 화면 밖으로 나가지 않도록 좌표 조정
    right_heart_x = max(0, min(right_heart_x, w - heart_resized01.shape[1]))
    right_heart_y = max(0, min(right_heart_y, h - heart_resized01.shape[0]))
    left_heart_x = max(0, min(left_heart_x, w - heart_resized02.shape[1]))
    left_heart_y = max(0, min(left_heart_y, h - heart_resized02.shape[0])) 
         

    frame = overlay_image(frame, heart_resized01, right_heart_x, right_heart_y, angle)
    frame = overlay_image(frame, heart_resized02, left_heart_x, left_heart_y, angle)
    
    return frame
