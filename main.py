import cv2
import numpy as np
import pyautogui
import win32gui
import keyboard
from PIL import ImageGrab
from dotenv import load_dotenv

load_dotenv()

toplist, winlist = [], []

def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, [])

def bring_spotify_to_foreground():
    spotify_app = [(hwnd, title) for hwnd, title in winlist if 'spotify' in title.lower()]
    if spotify_app:
        hwnd = spotify_app[0][0]
        win32gui.SetForegroundWindow(hwnd)
        bbox = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(bbox)
        img.save('screenshot.png')

img_path = 'screenshot.png'

spotify_not_found_count = 0

running = True
stop_key = None

def on_any_key_press(e):
    global running, stop_key
    if e.name.isalnum():
        running = False
        stop_key = e.name

keyboard.on_press(on_any_key_press)

while running:
    bring_spotify_to_foreground()

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    template = cv2.imread('spotify_logo.png',0)

    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)

    found_spotify = False
    coordinates = []
    min_distance_pct = 0.1
    min_distance = img.shape[1] * min_distance_pct

    w, h = template.shape[::-1]

    for pt in zip(*loc[::-1]):
        if not any(np.sqrt((pt[0] - x)**2 + (pt[1] - y)**2) < min_distance for (x, y) in coordinates):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
            print("Logo found at: ", pt)
            coordinates.append(pt)
            found_spotify = True

    if not found_spotify:
        spotify_not_found_count += 1
    else:
        spotify_not_found_count = 0

    if spotify_not_found_count >= 5:
        break


    # for (x, y) in coordinates:
    #     screen_x = x
    #     screen_y = y
    #     pyautogui.moveTo(screen_x, screen_y)
    #     pyautogui.keyDown('ctrl')
    #     pyautogui.click()
    #     pyautogui.keyUp('ctrl')

    pyautogui.scroll(-980)
    cv2.imwrite('annotated_image.png', img)

if stop_key != None:
    print(f"Program stopped after pressing '{stop_key}' key.")
