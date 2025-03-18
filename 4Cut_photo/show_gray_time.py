import cv2
import numpy as np
from PIL import Image
import time
import datetime

#5초가 지나면 자동으로 cap_case
start_grayscale = None

# 4단계 : 흑백모드  
def show_grayscale(frame):
    global start_grayscale
    cap_case = False
    
    if start_grayscale is None:
        start_grayscale = time.time()
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
    
    elapsed_time = time.time() - start_grayscale
    
    if elapsed_time >= 4:
       cap_case = True  

    return frame, cap_case   

# 4단계 사진촬영 후 흑백모드 초기화
def reset_start():
    global start_grayscale
    start_grayscale = None
       
# 4단계 : 현재시간 화면에 출력하기
def add_datetime(frame):
    # print ("current time is %s." % (str(datetime.now())))
    
    #현재 시각 확보
    now = time.localtime()
    
    #AM or PM 정하기
    if now.tm_hour <13:
        AM_or_PM = ' AM'
        t_hour = "%02d" %(now.tm_hour)
    else:
        AM_or_PM = ' PM'
        t_hour = "%02d"%(now.tm_hour-12)
        
    #분, 초
    t_min = "%02d"%(now.tm_min)
    t_sec = "%02d"%(now.tm_sec)
    
    #월, 일, 년
    s = "%04d.%02d.%02d"%(now.tm_year, now.tm_mon, now.tm_mday)
    dt = datetime.datetime.strptime(s, '%Y.%m.%d')
    first_line = t_hour + ':'+ t_min + ':' + t_sec + AM_or_PM + " "
    second_line = dt.strftime('%Y.%m.%d ')
    
    cv2.putText(frame, second_line + first_line, (50, 430), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 2)
            
    return frame
