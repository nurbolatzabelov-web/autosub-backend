from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

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
    files = {
        "data": (
            video.filename,
            await video.read(),
            video.content_type
        )
    }

    payload = {
        "language": language,
        "punctuation": "true",
        "burn_subtitles": "false"
    }

    response = requests.post(
        HF_API_URL,
        files=files,
        data=payload,
        timeout=300
    )

    return response.json()
