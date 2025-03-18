# Project01
mediapipe를 활용한 인생네컷 ( 4 photos using MediaPipe )

# 4Cut Photo Project

이 프로젝트는 다양한 사진 촬영 기능과 이미지를 합성하는 기능을 제공합니다. 주요 기능으로는 **세로 자르기**, **프레임 추가**, **윙크 인식**, **그레이스케일 타이머** 등이 있으며, 여러 장의 사진을 합쳐 하나의 합성된 이미지를 생성할 수 있습니다.

## 프로젝트 구성
```
📦4Cut_photo
 ┣ 📂output
 ┣ 📂resources
 ┃ ┣ 📜basic.png
 ┃ ┣ 📜frame1.jpg
 ┃ ┣ 📜frame2.jpg
 ┃ ┣ 📜frame3.jpg
 ┃ ┣ 📜frame4.jpg
 ┃ ┣ 📜frame4_1.png
 ┃ ┣ 📜frame4_2.jpg
 ┃ ┣ 📜heart.png
 ┃ ┣ 📜love.png
 ┃ ┣ 📜lucky.png
 ┃ ┗ 📜random.png
 ┣ 📂__pycache__
 ┃ ┣ 📜add_frame.cpython-39.pyc
 ┃ ┣ 📜add_heart_sticker.cpython-39.pyc
 ┃ ┣ 📜cut_veritical.cpython-39.pyc
 ┃ ┣ 📜detect_point_gesture.cpython-39.pyc
 ┃ ┣ 📜detect_v_gesture.cpython-39.pyc
 ┃ ┣ 📜detect_wink.cpython-39.pyc
 ┃ ┣ 📜select_frame.cpython-39.pyc
 ┃ ┣ 📜show_gray_time.cpython-39.pyc
 ┃ ┗ 📜show_selection_menu.cpython-39.pyc
 ┣ 📜add_frame.py
 ┣ 📜add_heart_sticker.py
 ┣ 📜cut_veritical.py
 ┣ 📜detect_point_gesture.py
 ┣ 📜detect_v_gesture.py
 ┣ 📜detect_wink.py
 ┣ 📜main.py
 ┣ 📜select_frame.py
 ┣ 📜show_gray_time.py
 ┗ 📜show_selection_menu.py
```

## 기능

- **프레임 추가 (add_frame.py)**: 사용자가 선택한 프레임 위에 촬영된 4장의 이미지를 합성합니다.
- **세로 자르기 (cut_vertical.py)**: 사진을 세로로 자르는 기능입니다.
- **윙크 인식 (detect_wink.py)**: 사용자가 윙크를 하면 자동으로 사진을 촬영합니다.
- **그레이스케일 타이머 (show_gray_time.py)**: 화면을 그레이스케일로 변환하고 3초 후에 사진을 촬영합니다.

## 실행 방법

1. `main.py` 파일을 실행하여 전체 기능을 통합적으로 사용합니다.
2. **설치**:
    ```bash
    pip install opencv-python numpy
    ```
3. **실행**:
    ```bash
    python main.py
    ```

## 디렉토리 설명

- **output/**: 촬영된 이미지와 합성된 이미지를 저장하는 폴더입니다.
- **resources/**: 프레임 이미지 및 아이콘 등을 저장하는 폴더입니다.
- **add_frame.py**: 이미지를 선택한 프레임으로 꾸미는 기능을 담당하는 파일입니다.
- **cut_vertical.py**: 이미지를 세로로 자르는 기능을 담당하는 파일입니다.
- **detect_wink.py**: 윙크를 인식하여 사진을 찍는 기능을 담당하는 파일입니다.
- **show_gray_time.py**: 화면을 그레이스케일로 변환하고, 타이머가 끝나면 사진을 찍는 기능을 담당하는 파일입니다.

## 사용 예시

1. **윙크로 사진 촬영**: 윙크를 하면 3초 후에 사진이 자동으로 촬영됩니다.
2. **그레이스케일 타이머**: 화면을 그레이스케일로 변경하고 3초 후 사진을 촬영합니다.
3. **프레임 추가**: 촬영된 사진에 선택한 프레임을 추가할 수 있습니다.
4. **사진 합성**: 여러 장의 촬영된 이미지를 하나로 합성하여 저장할 수 있습니다.

