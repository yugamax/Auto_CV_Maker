import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import pdfplumber
from html_gen import gen_res
from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright
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
    if os.path.exists("resume.html"):
        os.remove("resume.html")

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

async def pdf_write(text):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("resume_template.html")
    if isinstance(text, str):
        text = json.loads(text)
    rendered_html = template.render(**text)

    with open("resume.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        file_url = f"file://{os.path.abspath('resume.html')}"
        await page.goto(file_url)
        await page.pdf(path="resume.pdf", format="A4", print_background=True, margin= {"top": "0in", "bottom": "0in", "left": "0in", "right": "0in"})
        await browser.close()


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
    await pdf_write(html_str)
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
    await pdf_write(html_str)
    return FileResponse("resume.pdf", media_type="application/pdf", filename="resume.pdf")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="127.0.0.1", port=port)
