from pathlib import Path
from preliminary.library_basics import CodingVideo
from library_basics import path_checker

VID_PATH = Path("../resources/oop.mp4")

@path_checker
def test_path_checker(abs_path):
    """Try out your class here"""
    video_path = Path(abs_path)
    oop = CodingVideo(video_path)
    print(oop)
    image = oop.save_as_image(42)
    print(oop.get_text_of_image(image.get('image')))

if __name__ == "__main__":
    test_path_checker(VID_PATH)