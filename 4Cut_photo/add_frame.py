import cv2
import os
import time
from PIL import Image

# 현재 스크립트 위치 기준 output 폴더 경로 설정
base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, 'output')
resources_dir = os.path.join(base_dir, 'resources')

### 4장의 이미지를 선택된 프레임위에 얹기 ###
def add_frame(icon_index, img_cv):
    global img1, img2, img3, img4
       
    #캡쳐된 이미지 4장 (반복될때마다 초기화됨)
    img1 = Image.open(os.path.join(output_dir,"captured_image1.jpg"))
    img2 = Image.open(os.path.join(output_dir,"captured_image2.jpg"))
    img3 = Image.open(os.path.join(output_dir,"captured_image3.jpg"))
    img4 = Image.open(os.path.join(output_dir,"captured_image4.jpg"))
    
    img1_v = Image.open(os.path.join(output_dir,"vertical_captured_image1.jpg"))
    img2_v = Image.open(os.path.join(output_dir,"vertical_captured_image2.jpg"))
    img3_v = Image.open(os.path.join(output_dir,"vertical_captured_image3.jpg"))
    img4_v = Image.open(os.path.join(output_dir,"vertical_captured_image4.jpg"))

    #배경 이미지 4장 -> 전역변수로 사용x icon_index값에 따라 그때그때 불러옴
    #이미지 확인 (오류 확인)
    if img1 and img2 and img3 and img4 is None:
        print("이미지를 불러올 수 없습니다.")

    if icon_index == 0 : # basic 기본
        frame1 = Image.open(os.path.join(resources_dir, "frame1.jpg")) #452*1308
        gap = 20
        scale = 0.6
        new_width =int(img1.width * scale)
        new_height = int(img1.height * scale)
        
        img1 = img1.resize((new_width, new_height))
        img2 = img2.resize((new_width, new_height))
        img3 = img3.resize((new_width, new_height))
        img4 = img4.resize((new_width, new_height))

        x = (frame1.width - img1.width) //2

        frame1.paste(img1, (x, gap))
        frame1.paste(img2, (x, gap*2 + new_height))
        frame1.paste(img3, (x, gap*3 + new_height*2))
        frame1.paste(img4, (x, gap*4 + new_height*3))

        frame1.save(os.path.join(output_dir, "frame1_result.jpg"))
        img_cv = cv2.imread(os.path.join(output_dir, "frame1_result.jpg"))
  
    elif icon_index == 1: # lucky
        frame2 = Image.open(os.path.join(resources_dir, "frame2.jpg")) #1080*1609
        gap = 56
        scale = 0.8
        new_width = int(img1.width * scale)
        new_height = int(img1.height *scale)
        img1 = img1.resize((new_width, new_height))
        img2 = img2.resize((new_width, new_height))
        img3 = img3.resize((new_width, new_height))
        img4 = img4.resize((new_width, new_height))
        
        frame2.paste(img1, (0, gap))
        frame2.paste(img2, (gap + new_width, gap))
        frame2.paste(img3, (0, gap*2 + new_height))
        frame2.paste(img4, (gap + new_width, gap*2 + new_height))
        
        frame2.save(os.path.join(output_dir, "frame2_result.jpg"))
        img_cv = cv2.imread(os.path.join(output_dir, "frame2_result.jpg"))
        img_cv = resize_frame(img_cv)

    elif icon_index == 2: # love, 춘식 세로ver
        frame3 = Image.open(os.path.join(resources_dir, "frame3.jpg")) #1794*2688 -> 837*1344 크기변경
        scale = 0.7
        gap = 40
        
        new_width = int(img1_v.width * scale)
        new_height = int(img1_v.height *scale)
        
        img1_v = img1_v.resize((new_width, new_height))
        img2_v = img2_v.resize((new_width, new_height))
        img3_v = img3_v.resize((new_width, new_height))
        img4_v = img4_v.resize((new_width, new_height))
        
        
        x_offset = (frame3.width - img1_v.width*2 - gap) //2
        y_offset = 350
        
        frame3.paste(img1_v, (x_offset, y_offset))
        frame3.paste(img2_v, (x_offset + gap + img1_v.width, y_offset ))
        frame3.paste(img3_v, (x_offset, y_offset + 80 + img1_v.height))
        frame3.paste(img4_v, (x_offset + gap + img1_v.width, y_offset + 80 + img1_v.height))
        
        frame3.save(os.path.join(output_dir, "frame3_result.jpg"))
        img_cv = cv2.imread(os.path.join(output_dir, "frame3_result.jpg"))
            
        
    elif icon_index == 3: # 랜덤 mix        
        frame4 = Image.open(os.path.join(resources_dir, "frame4.jpg")) #1300*1155
        
        gap = 40
        small_gap =15
        scale = 0.5
        
        new_width = int(img4.width * scale)
        new_height = int(img4.height * scale)
        
        # 1,3번 큰사이즈 이미지 & 배치
        frame4.paste(img1, (gap, gap))
        frame4.paste(img3, (gap, gap*2 + img1.height))
        
        new_width =int(img1.width * scale)
        new_height = int(img1.height * scale)
        
        img1_resize = img1.resize((new_width, new_height))
        img2_resize = img2.resize((new_width, new_height))
        img3_resize = img3.resize((new_width, new_height))
        img4_resize = img4.resize((new_width, new_height))
        
        x_offset = gap*2 + img1.width
        frame4.paste(img1_resize, (x_offset, gap))
        frame4.paste(img2_resize, (x_offset, gap + small_gap + img1_resize.height))
        frame4.paste(img3_resize, (x_offset, gap + small_gap*2 + img1_resize.height *2))
        frame4.paste(img4_resize, (x_offset, gap + small_gap*3 + img1_resize.height *3))
    
        frame4.save(os.path.join(output_dir, "frame4_result.jpg"))    
        img_cv = cv2.imread(os.path.join(output_dir, "frame4_result.jpg"))
        
        #png 파일 불러오기
        frame4_1 = cv2.imread(os.path.join(resources_dir, "frame4_1.png", cv2.IMREAD_UNCHANGED))
        if frame4_1.shape[2] == 4:
            b, g, r, a = cv2.split(frame4_1)
            alpha = a /255.0
        else :
            print("png 이미지에 알파 채널x")
            
        x, y = 1100,0
        h, w = frame4_1.shape[:2]
        roi = img_cv[y:y+h, x:x+w]
        
        for c in range(3):  # B, G, R 채널 합성
            roi[:, :, c] = (1 - alpha) * roi[:, :, c] + alpha * frame4_1[:, :, c]
        img_cv[y:y+h, x:x+w] = roi
        
        cv2.imwrite(os.path.join(output_dir, "frame4_result.jpg", img_cv))
        img_cv = resize_frame(img_cv)
    
    return img_cv, icon_index       

#배경 원본 이미지 크기 조절
def resize_frame(img_cv):
    h, w = img_cv.shape[:2]
    
    scale = 0.7
    new_w, new_h = int(w*scale), int(h*scale)
    
    img_cv = cv2.resize(img_cv, (new_w, new_h))
    
    return img_cv        

start_time = None
count_text = ""
select_detected = False

#프레임 선택을 위한 카운트다운. 검지 손 끝이 아이콘에 3초이상 머무를 경우 선택
def countdown_selection(frame, icon_index, select_case, cap_stage):
    global select_detected, start_time, count_text 
    
    if select_case and not select_detected :
        select_detected = True
        start_time = time.time()
        print("3초 카운트시작! 프레임이 선택됩니다")
        
    if select_detected:
        if start_time is None:
            start_time = time.time()
        elapsed_time = time.time() - start_time
        
        if elapsed_time < 1:
            count_text = ""
        elif elapsed_time < 1.8:
            count_text = "3"
        elif elapsed_time < 2.4:
            count_text = "2"
        elif elapsed_time <3.2 :
            count_text = "1"
        else:
            cap_stage = 5
            select_detected = False
            start_time = None
            count_text = ""
            
    if not select_case and select_detected:
        select_detected = False
        start_time = None
        count_text = ""
        
    cv2.putText(frame, count_text, (320, 240), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 5, cv2.LINE_AA)   

    return frame, icon_index, cap_stage