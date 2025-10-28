"""A basic introduction to Open CV

Instructions
------------

Implement the functions below based on their docstrings.

Notice some docstrings include references to third-party documentation
Some docstrings **require** you to add references to third-party documentation.

Make sure you read the docstrings C.A.R.E.F.U.L.Y (yes, I took the L to check that you are awake!)
"""

from PIL import Image
from pathlib import Path
import cv2
import numpy as np
import pytesseract

VID_PATH = Path("../resources/oop.mp4")
OUT_PATH = Path("../resources")
tesseract_cmd_path = "C:/Users/wrayth/source/repos/Tesseract-OCR/tesseract.exe"

class CodingVideo:
    capture: cv2.VideoCapture

    def __init__(self, video: Path | str):
        self.capture = cv2.VideoCapture(video)  # You complete me!
        if not self.capture.isOpened():
            raise ValueError(f"Cannot open {video}")

        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.frame_count = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.frame_count / self.fps

    def __str__(self) -> str:
        """Displays key metadata from the video

        Specifically, the following information is shown:
            FPS - Number of frames per second rounded to two decimal points
            FRAME COUNT - The total number of frames in the video
            DURATION (minutes) - Calculated total duration of the video given FPS and FRAME COUNT

        Reference
        ----------
        https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#gaeb8dd9c89c10a5c63c139bf7c4f5704d
        """
        return (f"Video is {round(self.duration / 60, 2)} minutes long, "
                f"with {self.frame_count} total frames, at {round(self.fps, 2)} FPS")

    def get_frame_number_at_time(self, seconds: int) -> int:
        """Given a time in seconds, returns the value of the nearest frame"""
        return int(seconds * self.fps)

    def get_frame_rgb_array(self, frame_number: int) -> np.ndarray:
        """Returns a numpy N-dimensional array (ndarray)

        The array represents the RGB values of each pixel in a given frame

        Note: cv2 defaults to BGR format, so this function converts the color space to RGB
        """
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
        ok, frame = self.capture.read()
        if not ok:
            raise ValueError("Unable to read frame from file")
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def get_image_as_bytes(self, seconds: int) -> bytes:
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.get_frame_number_at_time(seconds))
        ok, frame = self.capture.read()
        if not ok or frame is None:
            raise ValueError("Invalid frame in target location")
        ok, buf = cv2.imencode(".png", frame)
        if not ok:
            raise ValueError("Failed to encode frame")
        return buf.tobytes()

    def save_as_image(self, seconds: int, output_path: Path | str = 'output.png') -> Image:
        """Saves the given frame as a png image"""
        if type(output_path) is str:
            output_path = OUT_PATH / output_path

        frame = self.get_frame_number_at_time(seconds)
        frame = self.get_frame_rgb_array(frame)
        image = Image.fromarray(frame)
        image.save(output_path)
        return image

    def get_text_of_image(self, image: Image) -> str:
        """Currently not working"""
        return pytesseract.image_to_string(image)

def test():
    """Try out your class here"""
    oop = CodingVideo(VID_PATH)
    print(oop)
    image = oop.save_as_image(42)
    #print(oop.get_text_of_image(image))


if __name__ == '__main__':
    test()
