<center>

# **Spotify OCR Automation**

</center>

This program, designed with the purpose of selecting songs added by Spotify when the enhancement feature is turned on in your playlists, employs OCR (Optical Character Recognition) to automate interactions with the Spotify application. It captures a screenshot of the Spotify window, performs text recognition to locate specific elements, and simulates mouse clicks to interact with these identified elements.


![](https://github.com/mapleleafu/spotify_enhanced/blob/main/gif.gif)


# Prerequisites
- Python 3.7 or above
- Tesseract OCR Engine installed (https://github.com/tesseract-ocr/tesseract)
# Installation
1. Clone the repository:

```
git clone https://github.com/mapleleafu/spotify_enhanced
```
2. Change into the project directory:

```
spotify_enhanced
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```
4. Set up the environment variables:

- Create a `.env` file in the project directory.

- Open the `.env` file and add the following line, replacing `<path_to_tesseract_executable>` with the actual path to the Tesseract executable file on your system:

```
PATH_TES=<path_to_tesseract_executable>
```
5. Run the program:

```
python main.py
```
# Usage
1. Make sure Spotify is running and visible on your screen.

2. The program will automatically locate the Spotify window and capture a screenshot.

3. It will perform OCR on the screenshot to identify elements matching the pattern defined in the code.

4. If the pattern is found, the program will simulate mouse clicks on the identified elements.

5. The process will continue until the pattern is not found for two consecutive iterations.

6. Press any key to stop the program.

# Customization

- You can modify the `pixel_coordinates` variable to define the pixel coordinates of a specific area within the Spotify window to capture in the screenshot. Adjust it according to your requirements.

- Update the `pattern` variable to define a different pattern to match elements in the Spotify window. This pattern is used to filter out non-relevant elements.

- Modify the `wx` and `wy` variables to adjust the screen position for mouse clicks. These variables represent the offset from the top-left corner of the Spotify window.