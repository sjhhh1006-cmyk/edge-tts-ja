from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import edge_tts
import io
import urllib.parse

app = FastAPI()

@app.get("/tts")
async def tts(
    text: str = Query(...),
    voice: str = Query(default="ja-JP-NanamiNeural")
):
    print(f"收到原始text: {repr(text)}")
    decoded_text = urllib.parse.unquote(text)
    print(f"解码后text: {repr(decoded_text)}")
    communicate = edge_tts.Communicate(decoded_text, voice)
    audio_buffer = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])
    audio_buffer.seek(0)
    return StreamingResponse(audio_buffer, media_type="audio/mpeg")
