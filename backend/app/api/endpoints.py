from fastapi import APIRouter, File, UploadFile
from app.core import audio_processing

router = APIRouter()

@router.post("/analyze-song")
async def analyze_song(file: UploadFile = File(...)):
    # Process the uploaded file
    features = await audio_processing.extract_features(file.file)
    similar_songs = audio_processing.find_similar_songs(features)
    return {"similar_songs": similar_songs}
