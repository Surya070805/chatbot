from fastapi import FastAPI, Form, UploadFile, File, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from deep_translator import GoogleTranslator
import os
import uuid

app = FastAPI()

# Templates and Static Files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
os.makedirs("uploads", exist_ok=True)


def translate_text(input_text, target_language):
    return GoogleTranslator(source="auto", target=target_language).translate(input_text)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/translate-text/")
async def translate_text_route(input_text: str = Form(...), target_language: str = Form(...)):
    translated_text = translate_text(input_text, target_language)
    word_count = len(input_text.split())

    if word_count <= 150:
        return templates.TemplateResponse(
            "index.html",
            {"request": {}, "translated_text": translated_text},
        )
    else:
        return templates.TemplateResponse(
            "output.html",
            {"request": {}, "original_text": input_text, "translated_text": translated_text},
        )


@app.post("/translate-file/")
async def translate_file_route(uploaded_file: UploadFile = File(...), target_language: str = Form(...)):
    # Save uploaded file
    file_id = str(uuid.uuid4())
    input_path = f"uploads/{file_id}_{uploaded_file.filename}"
    with open(input_path, "wb") as f:
        f.write(await uploaded_file.read())

    # Read and translate file
    with open(input_path, "r", encoding="utf-8") as f:
        file_content = f.read()
    translated_content = translate_text(file_content, target_language)

    # Save translated file
    output_path = f"uploads/{file_id}_translated.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(translated_content)

    return {"success": True, "download_url": output_path}


@app.get("/download/{file_path:path}")
async def download_file(file_path: str):
    return FileResponse(file_path, media_type="application/octet-stream", filename=file_path.split("/")[-1])
