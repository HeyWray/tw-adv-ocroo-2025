"""Provides a simple API for your basic OCR client

Drive the API to complete "interprocess communication"

Requirements
"""
from idlelib.debugger_r import DictProxy

from fastapi import FastAPI, HTTPException
from fastapi import Response
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from library_basics import CodingVideo
import cv2

app = FastAPI()

# We'll create a lightweight "database" for our videos
# You can add uploads later (not required for assessment)
# For now, we will just hardcode are samples
VIDEOS: dict[str, Path] = {
    "demo": Path("./resources/oop.mp4")
}


class VideoMetaData(BaseModel):
    fps: float
    frame_count: int
    duration_seconds: float
    _links: dict | None = None


@app.get("/")
def home():
    return FileResponse("pages/main.py")


@app.get("/video")
def list_videos():
    """List all available videos with HATEOAS-style links."""
    return {
        "count": len(VIDEOS),
        "videos": [
            {
                "id": vid,
                "path": str(path),  # Not standard for debug only
                "_links": {
                    "self": f"/video/{vid}",
                    "frame_example": f"/video/{vid}/frame/1.0"
                }
            }
            for vid, path in VIDEOS.items()
        ]
    }


def _open_vid_or_404(vid: str) -> CodingVideo:
    path = VIDEOS.get(vid)
    if not path or not path.is_file():
        raise HTTPException(status_code=404, detail="Video not found")
    try:
        return CodingVideo(path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Could not open video {e}")


def _meta(video: CodingVideo) -> VideoMetaData:
    return VideoMetaData(
        fps=video.fps,
        frame_count=video.frame_count,
        duration_seconds=video.duration
    )


@app.get("/video/{vid}", response_model=VideoMetaData)
def video_info(vid: str):
    """
    returns video information e.g. how long the video is
    """
    video = _open_vid_or_404(vid)
    try:
        meta = _meta(video)
        meta._links = {
            "self": f"/video/{vid}",
            "frames": f"/video/{vid}/frame/{{seconds}}"
        }
        return meta
    finally:
        video.capture.release()


@app.get("/video/{vid}/frame/{t}", response_class=Response)
def video_frame(vid: str, t: float):
    try:
        video = _open_vid_or_404(vid)
        return Response(content=video.get_image_as_bytes(t), media_type="image/png")
    finally:
        video.capture.release()


@app.get("/video/{vid}/frame/{t}/ocr")
def video_frame_ocr(vid: str, t: int):
    coding_vid = CodingVideo(VIDEOS[vid])
    image = coding_vid.save_as_image(t, VIDEOS[vid])
    return {coding_vid.get_text_of_image(image)
            .replace("\n", " \n ")}


@app.get("/video/path/{vid}")
def video_path(vid: str) -> Path|None:
    """
    Returns video file Path or None.
    Source: https://geekpython.in/stream-video-to-frontend-in-fastapi
    """

    e = _open_vid_or_404(vid)
    if (e is HTTPException):
        return print("Could not find the video")

    path = VIDEOS.get(vid)
    return path

@app.get("/video/playback/{vid}")
async def video_playback(vid: str) -> Path|None:
    """
    Returns video file Path or None.
    Source: https://geekpython.in/stream-video-to-frontend-in-fastapi
    """

    video = video_path(vid)
    if video is None:
        return None

    cap = cv2.VideoCapture(video)
    while (cap.isOpened()):

        ret, frame = cap.read()
        # cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        # cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if ret:
            cv2.imshow("Image", frame)
        else:
            print('no video')
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue


    cap.release()
    cv2.destroyAllWindows()
    return None