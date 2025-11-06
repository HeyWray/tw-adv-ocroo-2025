# Overview

This project is a project for TAFE intended to capture text from coding videos for a blind programming student. 

It uses OpenCV-Python for video preperation, Pillow for creating images, Tesseract for extracting text from images, and FastAPI for displaying a webased project.



## Requirements

### [Tesseract](https://tesseract-ocr.github.io/tessdoc/Compiling.html#windows)

Install for Windows
> git clone https://github.com/tesseract-ocr/tesseract tesseract

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



## How to Use

#### Running FastAPI
> uv run fastapi dev preliminary/simple_api.py 

You can now open https://127.0.0.1:8000/docs for a list of methods to use

The first method /test provides a starting point

#### Pass variables
- Input the full computer path to the video oop.mp4 located in the resources folder
- Input the time of the frame you would like to access in seconds (e.g. 1m30s would be 90)


You will now have:
- The text of the frame, outputted as a return string
- A .png screenshot saved of the frame (located in the resources' folder)


## Known Bugs

- tesseract_cmd_path (mac and win) are both unused. These will also require manual set up per user to create a path to their respective tesseracts.
- While running the project library_basics form inside your IDE you can use the relative path of the video, outside you must use the full path to point to the video
- Either using videos outside the project resources folder OR videos of type .mov will not work