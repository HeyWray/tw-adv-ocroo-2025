from PIL import Image
from pathlib import Path
from preliminary.library_basics import CodingVideo
import os
import unittest



VID_PATH = Path("../resources/oop.mp4")

class TestCodingVideo(unittest.TestCase):
    def test_valid_video(self):
        abs_path = os.path.abspath(VID_PATH)
        self.assertTrue(os.path.exists(abs_path))
        video = CodingVideo(Path(abs_path))
        self.assertGreater(video.fps, 0)
        self.assertGreater(video.frame_count, 0)

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            CodingVideo(Path("nonexistent.mp4"))


if __name__ == "__main__":
    unittest.main()
