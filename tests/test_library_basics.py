from PIL import Image
from pathlib import Path
from preliminary.library_basics import CodingVideo, VID_PATH
from library_basics import path_checker
import unittest


@path_checker
def test_path_checker(VID_PATH):
    """Try out your class here"""
    oop = CodingVideo(VID_PATH)
    print(oop)
    image = oop.save_as_image(42)
    print(oop.get_text_of_image(image.get('image')))


class TestCodingVideo(unittest.TestCase):

    def test_valid_video(self):
        VID_PATH = Path("../resources/oop.mp4")
        video = CodingVideo(VID_PATH)
        self.assertGreater(video.fps, 0)
        self.assertGreater(video.frame_count, 0)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            CodingVideo(Path("../resources/nonexistent.mp4"))


if __name__ == "__main__":
    unittest.main()
