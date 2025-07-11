import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import pdfplumber
from html_gen import gen_res
from jinja2 import Environment
import pdfkit

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

def pdf_read():
    try:
        with pdfplumber.open("temp_resume.pdf") as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                return text
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.api_route("/ping", methods=["GET", "HEAD"])
async def ping():
    await asyncio.sleep(0.1)
    return {"message": "server is running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "File must be a PDF."})
    
    contents = await file.read()
    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)

    text = pdf_read()
        
    html_str = gen_res(text)
    pdfkit.from_string(html_str, "resume.pdf")

    
@app.post("/upl_chat")
async def upload_pdf(file: UploadFile = File(...), prompt: str = Form(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "File must be a PDF."})
    
    contents = await file.read()
    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)
        
    text = pdf_read()

    html_str = gen_res(text, prompt)
    pdfkit.from_string(html_str, "resume.pdf")

