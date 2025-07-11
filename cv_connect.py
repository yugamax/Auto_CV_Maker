import os
from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from dotenv import load_dotenv
import pdfplumber
from groq import Groq
import prompts

load_dotenv()
client = Groq(api_key=os.getenv("gr_api_key"))


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

chat_hist = [{"role": "system", "content": prompts.prompt}]

@app.api_route("/ping", methods=["GET", "HEAD"])
async def ping():
    await asyncio.sleep(0.1)
    return {"message": "server is running"}

# WebSocket endpoint for chat and PDF upload
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    global chat_hist
    try:
        while True:
            data = await websocket.receive_json()
            # Expecting {"type": "pdf", "file": <bytes>} or {"type": "chat", "msg": <str>}
            if data.get("type") == "pdf":
                pdf_bytes = bytes(data.get("file"))
                with open("temp.pdf", "wb") as f:
                    f.write(pdf_bytes)
                try:
                    with pdfplumber.open("temp.pdf") as pdf:
                        text = "\n".join([page.extract_text() or "" for page in pdf.pages])
                    await websocket.send_json({"type": "pdf_text", "text": text})
                except Exception as e:
                    await websocket.send_json({"type": "error", "error": str(e)})
            elif data.get("type") == "chat":
                ui_msg = data.get("msg", "")
                chat_hist.append({"role": "user", "content": ui_msg})
                try:
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=chat_hist,
                        temperature=0.2,
                        max_tokens=512,
                    )
                    res = completion.choices[0].message.content
                    chat_hist.append({"role": "assistant", "content": res})
                    await websocket.send_json({"type": "chat_response", "response": res})
                except Exception as e:
                    await websocket.send_json({"type": "error", "error": str(e)})
    except WebSocketDisconnect:
        pass
