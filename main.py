import cv2
import re
import pyautogui
import win32gui
import keyboard
import os
from pytesseract import pytesseract, Output
from PIL import ImageGrab
from dotenv import load_dotenv

load_dotenv()

#! Define Tesseract path here or in the .env file
path_tes = os.getenv("PATH_TES")
pytesseract.tesseract_cmd = path_tes

toplist, winlist = [], []
pixel_coordinates = (1300, 0, 1470, 0) #! Define pixel coordinates of the "Added by" column

def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, [])

def bring_spotify_to_foreground(pixel_coordinates):
    spotify_app = [(hwnd, title) for hwnd, title in winlist if 'spotify' in title.lower()]
    if spotify_app:
        hwnd = spotify_app[0][0]
        win32gui.SetForegroundWindow(hwnd)
        bbox = win32gui.GetWindowRect(hwnd)
        img = ImageGrab.grab(bbox)
        pixel_coordinates = (pixel_coordinates[0], pixel_coordinates[1], pixel_coordinates[2], img.size[1])
        cropped_img = img.crop(pixel_coordinates)
        cropped_img.save('cropped_screenshot.png')
    else:
        print("Spotify app not found.")

img_path = 'cropped_screenshot.png'

# The following re is used to find the word 'Spotify' or relative words in the image
pattern = re.compile('s[pb]?o?[t1l]?i?[tf]?[iy]?|sin|sity|ss', re.IGNORECASE)

spotify_not_found_count = 0


running = True
stop_key = None

# Define a callback for any key
def on_any_key_press(e):
    global running, stop_key
    if e.name.isalnum():
        running = False
        stop_key = e.name


keyboard.on_press(on_any_key_press)

while running:
    bring_spotify_to_foreground(pixel_coordinates)

    img = cv2.imread(img_path)  

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Perform OCR on the image
    image_data = pytesseract.image_to_data(img, output_type=Output.DICT, config='--oem 3 --psm 6')

    coordinates = []

    found_spotify = False  # Variable to check if 'Spotify' was found in the current iteration

    for i, word in enumerate(image_data['text']):
        if pattern.match(word):
            x, y, w, h = image_data['left'][i], image_data['top'][i], image_data['width'][i], image_data['height'][i]
            coordinates.append((x, y, w, h))
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(img, word, (x - 60, y - 16), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
            print("Predicted text:", word)
            found_spotify = True  

    if not found_spotify:
        spotify_not_found_count += 1
    else:
        spotify_not_found_count = 0

    if spotify_not_found_count >= 5:
        print("Spotify text not found after 5 scrolls. Stopping the program.")
        break

    # Sort the coordinates from top to bottom
    coordinates.sort(key=lambda x: x[1])

    for (x, y, w, h) in coordinates:
        screen_x = x + pixel_coordinates[0]
        screen_y = y
        pyautogui.moveTo(screen_x, screen_y)
        pyautogui.keyDown('ctrl')
        pyautogui.click()
        pyautogui.keyUp('ctrl')

    #! Replace this with the total pixel amount required to scroll through an entire page
    pyautogui.scroll(-980)
    
    if found_spotify == True:
        cv2.imwrite('annotified_image.png', img)
    pass  

if stop_key != None:
    print(f"Program stopped after pressing '{stop_key}' key.")