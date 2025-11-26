"""Provides a simple API for your basic OCR client

Drive the API to complete "interprocess communication"

Requirements
"""
import os
import sys
sys.path.insert(0, "../resources")
from fastapi import FastAPI, HTTPException
from fastapi import Response
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from library_basics import CodingVideo
import cv2

app = FastAPI()


VIDEOS = {
    "Classes" : {
        'id' : "Classes",
        'path' : Path("resources/oop.mp4"),
        'description' : "A fundamental look at the basics of classes"
    },
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
    """
    List all available videos with HATEOAS-style links.
    returns dict
    """
    return {
        "count": len(VIDEOS),
        "videos": [
            {
                "id": VIDEOS.get(vid).get('id'),
                "path": str(VIDEOS.get(vid).get('path')),  # Not standard for debug only
                "_links": {
                    "self": f"/video/{vid}",
                    "frame_example": f"/video/{vid}/frame/1.0"
                },
                "description": VIDEOS.get(vid).get('description')
            }
            for vid in VIDEOS
        ]
    }


def _open_vid_or_404(vid: str) -> CodingVideo:
    path = VIDEOS.get(vid).get('path')

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
        video_or_404 = _open_vid_or_404(vid)
        return Response(content=video_or_404.get_image_as_bytes(t), media_type="image/png")
    finally:
        video_or_404.capture.release()


@app.get("/video/{vid}/frame/{t}/ocr")
def video_frame_ocr(vid: str, t: int):
    #encode the video
    coding_vid = CodingVideo(VIDEOS.get(vid).get('path'))

    #create an image from the extracted video
    image = coding_vid.save_as_image(t, VIDEOS.get(vid).get('path'))

    #get the text from the image
    text = {coding_vid.get_text_of_image(image.get('image'))
            .replace("\n", " \n ")}

    #delete the image
    os.remove(image.get('path'))
    return text


@app.get("/video/path/{vid}")
def video_path(vid: str) -> Path|None:
    """
    Returns video file Path or None.
    Source: https://geekpython.in/stream-video-to-frontend-in-fastapi
    """
    e = _open_vid_or_404(vid)
    if (e is HTTPException):
        return print("Could not find the video")

    path = VIDEOS.get(vid).get('path')
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
