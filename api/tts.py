from http.server import BaseHTTPRequestHandler
import urllib.parse
import asyncio
import edge_tts

async def amain(text, writer):
    # 锁定日语音色，直接调用官方 edge_tts 库以确保 100% 绕过签名限制
    communicate = edge_tts.Communicate(text, "ja-JP-NanamiNeural")
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            writer.write(chunk["data"])

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 解析前端传过来的文本参数
        url_parts = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(url_parts.query)
        text = query.get('text', [''])[0]

        if not text:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing text parameter")
            return

        self.send_response(200)
        self.send_header('Content-type', 'audio/mpeg')
        # 允许你的 GitHub Pages 跨域调用
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # 运行异步合成逻辑
        asyncio.run(amain(text, self.wfile))
        return
app = handler
