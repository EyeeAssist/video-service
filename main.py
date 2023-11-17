from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from auth.auth_service import api_key_auth
from video.video_entity import Video
from video.video_service import is_youtube_url, download_video, read_video
from image.image_service import process_image
from googletrans import Translator
translator = Translator()


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
        path = download_video(video.link)
        video_frames = read_video(path)
        result = []
        for frame in video_frames:
            print('Describing image in the second -> ', frame['time'])
            description = process_image(frame['frame_image'])
            print('Description ->', description)
            translated = translator.translate(description, dest='es')
            result.append({'time': frame['time'],
                           'description': translated[0].text})
        return {"video": result}
    else:
        raise HTTPException(status_code=400, detail="El link no es un link de youtube valido")
