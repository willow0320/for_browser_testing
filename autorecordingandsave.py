import time
import os
import pyautogui
import numpy as np
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Chrome 드라이버 설치 후 초기화
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Chrome WebDriver 옵션 설정
options = Options()
options.add_argument("--start-maximized")

# 설정한 옵션을 적용하여 Chrome을 실행
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# URL 리스트 파일 경로
url_list_file = '/Users/willow/Project/screen-record-and-save/test_urls.txt'

# URL 리스트 파일 읽기
with open(url_list_file, 'r') as file:
    urls = file.read().splitlines()

# 비디오 파일 저장 설정
frames_per_second = 10
screen_size = pyautogui.size()
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# 녹화 영상 저장 경로
output_directory = '/Users/willow/Project/screen-record-and-save/recordings/'

# 초기화
recorded_videos = 0
current_url = ''

while True:
    new_url = driver.current_url
    
    # URL이 변경되었거나 새로운 창이 열린 경우
    if new_url != current_url:
        current_url = new_url
        
        # URL이 test_urls.txt에 포함되어 있는지 확인
        if current_url in urls:
            # 비디오 파일 이름 설정 (yyyy-mm-dd hhmmss)
            timestamp = time.strftime("%Y-%m-%d_%H%M%S")
            video_file = f'{output_directory}recording_{timestamp}.mp4'
            out = cv2.VideoWriter(video_file, fourcc, frames_per_second, (screen_size.width, screen_size.height))

            start_time = time.time()
            while (time.time() - start_time) < 30:
                # Chrome 브라우저 창 위치 및 크기 가져오기
                browser_window = driver.get_window_rect()
                left = browser_window['x']
                top = browser_window['y']
                width = browser_window['width']
                height = browser_window['height']
                
                # 전체 화면 캡처 후 Chrome 브라우저 창 영역만 잘라냄
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                browser_frame = frame[top:top+height, left:left+width]
                
                out.write(browser_frame)
                time.sleep(1 / frames_per_second)

            out.release()
            recorded_videos += 1

            # 녹화 중인 영상이 20개가 되면 녹화 중지
            if recorded_videos >= 20:
                messagebox.showinfo("녹화 중지", "녹화가 완료되었습니다. 영상을 삭제하고 녹화를 중지합니다.")
                for filename in os.listdir(output_directory):
                    if filename.startswith("recording_") and filename.endswith(".mp4"):
                        os.system(f"mv '{output_directory}{filename}' ~/.Trash/")
                break

            # 팝업 창 표시 및 선택
            root = tk.Tk()
            root.withdraw()
            result = messagebox.askyesno("계속 녹화 여부", "녹화를 계속 진행하시겠습니까?")
            root.destroy()

            if not result:
                # 사용자가 "녹화 중지" 선택
                messagebox.showinfo("녹화 중지", "사용자가 녹화를 중지했습니다. 영상을 삭제하고 녹화를 중지합니다.")
                for filename in os.listdir(output_directory):
                    if filename.startswith("recording_") and filename.endswith(".mp4"):
                        os.system(f"mv '{output_directory}{filename}' ~/.Trash/")
                break
            else:
                # 사용자가 "녹화 진행" 선택
                continue

        else:
            continue

    time.sleep(1)

# 브라우저 종료
driver.quit()
