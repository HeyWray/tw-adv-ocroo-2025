from preliminary.library_basics import CodingVideo
from library_basics import path_checker

@path_checker
def test_path_checker(VID_PATH):
    """Try out your class here"""
    oop = CodingVideo(VID_PATH)
    print(oop)
    image = oop.save_as_image(42)
    print(oop.get_text_of_image(image.get('image')))

if __name__ == "__main__":
    test_path_checker("resources/oop.mp4")