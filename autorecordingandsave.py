import time
import os
import pyautogui
import numpy as np
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter import filedialog, messagebox

# Install and initialize Chrome driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Chrome WebDriver options setup
options = Options()
options.add_argument("--start-maximized")

# Launch Chrome with the specified options
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Prompt user to select URL list file
root = tk.Tk()
root.withdraw()
url_list_file = filedialog.askopenfilename(title="Select URL List File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
root.destroy()

if not url_list_file:
    messagebox.showerror("Error", "No URL list file selected. Exiting.")
    exit()

# Read the URL list file
with open(url_list_file, 'r') as file:
    urls = file.read().splitlines()

# Video recording settings
frames_per_second = 10
screen_size = pyautogui.size()
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# User-defined recording output directory
output_directory = '/path/to/your/custom/output/directory/'

# Initialization
recorded_videos = 0
current_url = ''

while True:
    new_url = driver.current_url
    
    # Check if URL has changed or a new window has opened
    if new_url != current_url:
        current_url = new_url
        
        # Check if the current URL is in the selected URL list
        if current_url in urls:
            # Set video file name (yyyy-mm-dd hhmmss)
            timestamp = time.strftime("%Y-%m-%d_%H%M%S")
            video_file = f'{output_directory}recording_{timestamp}.mp4'
            out = cv2.VideoWriter(video_file, fourcc, frames_per_second, (screen_size.width, screen_size.height))

            start_time = time.time()
            while (time.time() - start_time) < 30:
                # Get Chrome browser window position and size
                browser_window = driver.get_window_rect()
                left = browser_window['x']
                top = browser_window['y']
                width = browser_window['width']
                height = browser_window['height']
                
                # Capture entire screen and crop to Chrome browser window area
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                browser_frame = frame[top:top+height, left:left+width]
                
                out.write(browser_frame)
                time.sleep(1 / frames_per_second)

            out.release()
            recorded_videos += 1

            # Stop recording if 20 videos have been recorded
            if recorded_videos >= 20:
                messagebox.showinfo("Recording Stopped", "Recording complete. Deleting videos and stopping recording.")
                for filename in os.listdir(output_directory):
                    if filename.startswith("recording_") and filename.endswith(".mp4"):
                        os.system(f"mv '{output_directory}{filename}' ~/.Trash/")
                break

            # Display popup and prompt user
            root = tk.Tk()
            root.withdraw()
            result = messagebox.askyesno("Continue Recording?", "Do you want to continue recording?")
            root.destroy()

            if not result:
                # User clicked "Stop Recording"
                messagebox.showinfo("Recording Stopped", "User stopped recording. Deleting videos and stopping recording.")
                for filename in os.listdir(output_directory):
                    if filename.startswith("recording_") and filename.endswith(".mp4"):
                        os.system(f"mv '{output_directory}{filename}' ~/.Trash/")
                break
            else:
                # User clicked "Continue Recording"
                continue

        else:
            continue

    time.sleep(1)

# Quit the browser
driver.quit()
