# Overview

This project is a project for TAFE intended to capture text from coding videos for a blind programming student. 

It uses OpenCV-Python for video preperation, Pillow for creating images, Tesseract for extracting text from images, and FastAPI for displaying a webased project.



## Requirements

### [Tesseract](https://tesseract-ocr.github.io/tessdoc/Compiling.html#windows)

Install for Windows

There are several steps to this

1. Install [tesseract-ocr-w64-setup-5.5.0.20241111.exe](https://github.com/UB-Mannheim/tesseract/wiki)
2. During the installation process you will get a path file of where tesseract is downloading. e.g. `C:\Users\You\...\Tesseract-OCR...` Keep this on hand for later.
3. Continue with the 'Installation' step and come back to this point when asked.
4. Open `.venv/lib/python3.13/site-packages/pytesseract/pytesseract.py` (or equivalent)
5. Around line 32, change `tesseract_cmd` to be the file path to the tesseract.
6. Note, you need to make sure all `\` are converted to `/`
7. Be sure to add `/tesseract.exe` to the file path so we target tesseract's .exe specifically

Install for Mac
> brew install tesseract

### [Astral's uv](https://docs.astral.sh/uv/)

Install for Windows
> powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

Install for Mac/Linux
> curl -LsSf https://astral.sh/uv/install.sh | sh



## Installation

1. Install uv and Download Tesseract (see Requirements above)
2. cd to your source>repos or project folder location of choice
> cd [project folder]

3. Download this project
> git clone https://github.com/HeyWray/tw-adv-ocroo-2025.git

4. cd into the project `cd tw-adv-ocroo-2025`
5. Create a .venv in the project using uv 
> uv venv .venv
6. Install dependencies through uv 
> uv pip install -r pyproject.toml
7. Split your terminal or open another tab. Make sure you are in tw-adv-ocroo-2025.
8. If you are using windows please return back to the Tesseract download.


## Back End: Running FastAPI
> uv run fastapi dev preliminary/simple_api.py 

You can now open https://127.0.0.1:8000/docs for a list of methods to use

The first method /test provides a starting point


## Front End: Running Streamlit
> streamlit run main.py

You can now open http://localhost:8501 for the front end

For Streamlit documentation https://docs.streamlit.io/ 

## How to Use
You can either go into https://127.0.0.1:8000/docs or type in your CLI.

#### In browser 
Go into https://127.0.0.1:8000/docs

Press the blue bar `/video/{vid}/frame/{t}/ocr`

Press the button on the right 'Try it out'
Pass in the following for each variable

vid = `demo`

t = `42`

You will now see a response in the body along the lines of ["I finally saw The Matrix today..."]


#### In CLI
Type the following 

> curl -X 'GET' \
> 
> 'http://127.0.0.1:8000/video/demo/frame/42/ocr' \ 
> 
> -H 'accept: application/json'


## What is happening?
We are grabbing a frame from the video in `resources/oop.mp4` and seeing what text is on screen from the given time.

You can change the variable `t` to be any time in seconds and get a variety of text.

NOTE you will also get images from the video located in `resources/`

## Known Bugs

- tesseract_cmd_path (mac and win) are both unused. These will also require manual set up per user to create a path to their respective tesseracts.
- While running the project library_basics form inside your IDE you can use the relative path of the video, outside you must use the full path to point to the video
- Either using videos outside the project resources folder OR videos of type .mov will not work