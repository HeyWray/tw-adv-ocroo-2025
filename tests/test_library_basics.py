from PIL import Image
from pathlib import Path
from preliminary.library_basics import CodingVideo
from library_basics import path_checker
import unittest





class TestCodingVideo(unittest.TestCase):

    @path_checker
    def test_valid_video(self):
        VID_PATH = Path("./resources/oop.mp4")
        video = CodingVideo(VID_PATH)
        self.assertGreater(video.fps, 0)
        self.assertGreater(video.frame_count, 0)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            CodingVideo(Path("./resources/nonexistent.mp4"))

if __name__ == "__main__":
    unittest.main()
