import cv2
import numpy as np


# 4장의 사진 촬영 후 프레임 선택 화면 보여주기 


#아이콘 배치를 위한 변수 설정
x_offset = 90 #좌우 여백
y_offset = 340 #y축 시작점
icon_width = 100
icon_height = 100
gap = 20 #아이콘 간격

# 프레임 선택을 위한 흰색 불투명 배경 & 선택 글씨 표시
def show_selection_text(frame):
    overlay_frame = frame.copy()    
    h, w, _ = frame.shape
    
    #불투명 배경 생성
    white_bg = np.full((h, w, 3), (255, 255, 255), dtype=np.uint8)
    overlay_frame = cv2.addWeighted(overlay_frame, 0.5, white_bg, 0.5, 0)
    
    #font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(overlay_frame, "Select Layout", (80,70), font, 2, (0, 0, 0), 4, cv2.LINE_AA)  

    return overlay_frame 
    
# 프레임 선택을 위한 png icon 불러오기
def show_selection_icon(overlay_frame, icon_index):
        
    #아이콘 파일 불러오기
    icon_1 = cv2.imread("imgpng/basic.png", cv2.IMREAD_UNCHANGED)
    icon_2 = cv2.imread("imgpng/lucky.png", cv2.IMREAD_UNCHANGED)
    icon_3 = cv2.imread("imgpng/love.png", cv2.IMREAD_UNCHANGED)
    icon_4 = cv2.imread("imgpng/random.png", cv2.IMREAD_UNCHANGED)

    if icon_1 is None or icon_2 is None or icon_3 is None or icon_4 is None :
        print ("이미지 로드 실패")
        return overlay_frame    

    if icon_index == 0 : 
        icon_1 = cv2.resize(icon_1, (120,120), interpolation=cv2.INTER_AREA)
        icon_2 = cv2.resize(icon_2, (100,100), interpolation=cv2.INTER_AREA)
        icon_3 = cv2.resize(icon_3, (100,100), interpolation=cv2.INTER_AREA)
        icon_4 = cv2.resize(icon_4, (100,100), interpolation=cv2.INTER_AREA)    
        icons = [icon_1, icon_2, icon_3, icon_4]
        
    elif icon_index == 1 :
        icon_1 = cv2.resize(icon_1, (100,100), interpolation=cv2.INTER_AREA)
        icon_2 = cv2.resize(icon_2, (120,120), interpolation=cv2.INTER_AREA)
        icon_3 = cv2.resize(icon_3, (100,100), interpolation=cv2.INTER_AREA)
        icon_4 = cv2.resize(icon_4, (100,100), interpolation=cv2.INTER_AREA)    
        icons = [icon_1, icon_2, icon_3, icon_4]
        
    elif icon_index == 2 :
        icon_1 = cv2.resize(icon_1, (100,100), interpolation=cv2.INTER_AREA)
        icon_2 = cv2.resize(icon_2, (100,100), interpolation=cv2.INTER_AREA)
        icon_3 = cv2.resize(icon_3, (120,120), interpolation=cv2.INTER_AREA)
        icon_4 = cv2.resize(icon_4, (100,100), interpolation=cv2.INTER_AREA)    
        icons = [icon_1, icon_2, icon_3, icon_4]
        
    elif icon_index == 3 :
        icon_1 = cv2.resize(icon_1, (100,100), interpolation=cv2.INTER_AREA)
        icon_2 = cv2.resize(icon_2, (100,100), interpolation=cv2.INTER_AREA)
        icon_3 = cv2.resize(icon_3, (100,100), interpolation=cv2.INTER_AREA)
        icon_4 = cv2.resize(icon_4, (120,120), interpolation=cv2.INTER_AREA)    
        icons = [icon_1, icon_2, icon_3, icon_4]
        
    else :
        icon_1 = cv2.resize(icon_1, (100,100), interpolation=cv2.INTER_AREA)
        icon_2 = cv2.resize(icon_2, (100,100), interpolation=cv2.INTER_AREA)
        icon_3 = cv2.resize(icon_3, (100,100), interpolation=cv2.INTER_AREA)
        icon_4 = cv2.resize(icon_4, (100,100), interpolation=cv2.INTER_AREA)    
        icons = [icon_1, icon_2, icon_3, icon_4]

    select_case = icon_index == 0 or icon_index ==1 or icon_index == 2 or icon_index == 3

    #png 알파채널 제거해야함!  ! ! 
    for i, icon in enumerate(icons): #icon은 numpy 배열
        x = x_offset + i *(icon_width + gap)
        y = y_offset       
        
        if icon.shape[2] == 4: # !!! png경우 알파채널 값 4
            icon_rgb = icon[:, :, :3] # 0,1,2 번째 채널선택 -> RGB채널만 선택
            alpha = icon[:, :, 3] / 255.0  # 0~255 범위를 0~1로 정규화
            
            ##### 관심영역(ROI) 설정 -> icon의 실제 크기 사용 (icon 크기와 roi범위를 같게)
            #roi = overlay_frame[y:y+icon_height, x:x+icon_width]
            roi = overlay_frame[y:y+icon.shape[0], x:x+icon.shape[1]]
            
            # ROI 크기를 icon 크기로 변경
            roi_resized = cv2.resize(roi, (icon.shape[1], icon.shape[0]))

            ##### Alpha Blending 적용 (배경과 투명도 고려하여 합성)
            for c in range(3):  # B, G, R 채널 합성
                roi_resized[:, :, c] = (roi_resized[:, :, c] * (1 - alpha) + icon_rgb[:, :, c] * alpha).astype(np.uint8)
            
            # 합성된 영역을 원본 프레임에 반영
            overlay_frame[y:y+icon.shape[0], x:x+icon.shape[1]] = roi_resized
                    
        else :
            # JPG처럼 알파 채널 없는 경우 그냥 배치
            overlay_frame[y:y+icon_height, x:x+icon_width] = icon      
    return overlay_frame, icon_index, select_case

def get_icon_positions():
    icon_positions = {}
    
    for i in range(4):
        x = int(x_offset + i *(icon_width + gap))
        y = int(y_offset)
        
        icon_positions[f'icon_{i+1}'] = (x, y) #딕셔너리에 저장(for문안에 위치)
    return icon_positions
