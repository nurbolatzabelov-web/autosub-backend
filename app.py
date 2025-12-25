from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import requests
import base64

app = FastAPI()

# CORS (Netlify үшін)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_API_URL = "https://nuruk-autosub-app.hf.space/run/predict"

@app.post("/transcribe")
async def transcribe(
    video: UploadFile = File(...),
    language: str = Form("auto")
):
    # Видео оқу
    video_bytes = await video.read()

    # Base64
    video_base64 = base64.b64encode(video_bytes).decode("utf-8")

    payload = {
        "data": [
            {
                "name": video.filename,
                "data": video_base64
            },
            language,
            True,   # punctuation
            False,  # burn subtitles
            ""
        ]
    }

    # Hugging Face-ке жіберу
    response = requests.post(HF_API_URL, json=payload)

    return response.json()
