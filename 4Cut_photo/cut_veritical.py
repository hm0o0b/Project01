import cv2
import os
import mediapipe as mp

#Mediapipe설정하기
mp_face_mesh = mp.solutions.face_mesh

#현재 스크립트 위치 기준 output 폴더 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, 'output')
                        

#저장된 4장의 이미지 리스트(경로 포함)
captured_images= [os.path.join(output_dir, f"captured_image{i}.jpg") for i in range(1, 5)]

# 결과를 저장할 리스트
processed_images = []

#얼굴 중심 랜드마크
face_center_index = 195

# 세로버전으로 이미지 자르기 (사람 얼굴 중심점을 인식하여 인물 위주로 자름)
def cut_vertical():
    for captured_image in captured_images:
        image = cv2.imread(captured_image)
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        with mp_face_mesh.FaceMesh(max_num_faces=1) as face_mesh:
            face_results = face_mesh.process(img_rgb)
        
            if face_results.multi_face_landmarks:
                for face_landmarks in face_results.multi_face_landmarks:
                    h, w, _ = image.shape
                    face_center_landmark  = face_landmarks.landmark[face_center_index]
                    face_center_x = int(face_center_landmark.x *w)
                    
                    # face_center_x가 치우쳐져 있을 경우(최소, 최대값 설정)
                    if face_center_x - 210 < 0 :
                        output = image[:, :420]

                    elif face_center_x + 210 > w :
                        output = image[:, w-420:w]

                    else :
                        output = image[:, face_center_x - 210 : face_center_x + 210]
        
                    processed_images.append(output)
                    
                    # 세로버전으로 자른 후 다른이름으로 저장, 저장 경로 설정
                    file_name = os.path.basename(captured_image)
                    vertical_output_path = os.path.join(output_dir, f'vertical_{file_name}')
                    cv2.imwrite(vertical_output_path, output)
             