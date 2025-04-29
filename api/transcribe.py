from fastapi import APIRouter, UploadFile, File, HTTPException
import whisper
import tempfile
import os

router = APIRouter()

model = whisper.load_model("base")  

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        result = model.transcribe(tmp_path)

        os.remove(tmp_path)

        return {"transcription": result["text"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribing audio: {str(e)}")
