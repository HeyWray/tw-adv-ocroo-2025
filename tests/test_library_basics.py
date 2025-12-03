from PIL import Image
from pathlib import Path
from preliminary.library_basics import CodingVideo
import unittest


class TestCodingVideo(unittest.TestCase):
    def test_valid_video(self):
        video = CodingVideo(0)
        self.assertGreater(video.fps, 0)
        self.assertGreater(video.frame_count, 0)

if __name__ == "__main__":
    unittest.main()
