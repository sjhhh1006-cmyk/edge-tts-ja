from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import edge_tts
import io

app = FastAPI()

class TTSRequest(BaseModel):
    text: str
    voice: str = "ja-JP-NanamiNeural"

@app.post("/tts")
async def tts(req: TTSRequest):
    communicate = edge_tts.Communicate(req.text, req.voice)
    audio_buffer = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])
    audio_buffer.seek(0)
    return StreamingResponse(audio_buffer, media_type="audio/mpeg")
