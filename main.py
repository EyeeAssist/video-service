from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth.auth_service import api_key_auth
from video.video_entity import Video
from video.video_service import is_youtube_url, download_video


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/video", dependencies=[Depends(api_key_auth)])
async def process_video(video: Video):
    if is_youtube_url(video.link):
        download_video(video.link)
        return {"video": "Descargado"}
    else:
        raise HTTPException(status_code=400, detail="El link no es un link de youtube valido")
