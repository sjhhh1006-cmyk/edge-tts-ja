from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import edge_tts
import io

app = FastAPI()

@app.get("/tts")
async def tts(
    text: str = Query(...),
    voice: str = Query(default="ja-JP-NanamiNeural")
):
    communicate = edge_tts.Communicate(text, voice)
    audio_buffer = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])
    audio_buffer.seek(0)
    return StreamingResponse(audio_buffer, media_type="audio/mpeg")
