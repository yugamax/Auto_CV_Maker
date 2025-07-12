import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import pdfplumber
from html_gen import gen_res
import pdfkit
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

def check():
    if os.path.exists("resume.pdf"):
        os.remove("resume.pdf")
        print("File deleted.")

def pdf_read():
    try:
        with pdfplumber.open("temp_resume.pdf") as pdf:
            full_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n"
            return full_text.strip()

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def pdf_write(text):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("resume_template.html")
    rendered_html = template.render(**text)
    HTML(string=rendered_html).write_pdf("resume.pdf")

options = {
    "page-size": "A4",
    "margin-top": "0.3in",
    "margin-bottom": "0.3in",
    "margin-left": "0.2in",
    "margin-right": "0.2in",
    "encoding": "UTF-8",
    "quiet": "",
    "disable-smart-shrinking": "",
    "zoom": "0.9",
}


@app.api_route("/ping", methods=["GET", "HEAD"])
async def ping():
    await asyncio.sleep(0.1)
    return {"message": "server is running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    check()
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "File must be a PDF."})
    contents = await file.read()
    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)
    text = pdf_read()
    html_str = gen_res(text)
    os.remove("temp_resume.pdf")
    global options
    pdfkit.from_string(html_str, "resume.pdf", options=options)
    return FileResponse("resume.pdf", media_type="application/pdf", filename="resume.pdf")


@app.post("/upl_chat")
async def upload_pdf(file: UploadFile = File(...), prompt: str = Form(...)):
    check()
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"error": "File must be a PDF."})
    contents = await file.read()
    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)
    text = pdf_read()
    html_str = gen_res(text, prompt)
    os.remove("temp_resume.pdf")
    print(html_str)
    global options
    pdfkit.from_string(html_str, "resume.pdf", options=options)
    return FileResponse("resume.pdf", media_type="application/pdf", filename="resume.pdf")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="127.0.0.1", port=port)