# app/main.py
import os
import tempfile
import shutil
from fastapi import FastAPI, UploadFile, File
from google.cloud import documentai_v1 as documentai

app = FastAPI()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION", "us")  # "us" o "eu"
PROCESSOR_ID = os.getenv("GCP_PROCESSOR_ID")  # tu processor OCR
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

client = documentai.DocumentProcessorServiceClient()

@app.post("/ocr-pdf")
async def ocr_pdf(file: UploadFile = File(...)):
    # Guardar PDF temporalmente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    # Cargar contenido PDF
    with open(tmp_path, "rb") as f:
        pdf_bytes = f.read()

    raw_document = documentai.RawDocument(content=pdf_bytes, mime_type="application/pdf")

    # Construir request
    name = client.processor_path(PROJECT_ID, LOCATION, PROCESSOR_ID)
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    result = client.process_document(request=request)
    doc = result.document

    # Texto completo
    full_text = doc.text

    # Texto por páginas
    pages_text = []
    for page in doc.pages:
        start = page.layout.text_anchor.text_segments[0].start_index
        end = page.layout.text_anchor.text_segments[0].end_index
        pages_text.append(full_text[start:end])

    # Calcular confianza promedio
    confidences = []
    for page in doc.pages:
        for para in page.paragraphs:
            confidences.append(para.layout.confidence)
    avg_conf = sum(confidences) / len(confidences) if confidences else None

    return {
        "did_ocr": True,  # siempre corre OCR
        "pages": len(pages_text),
        "raw_text_per_page": pages_text,
        "raw_text": full_text,
        "avg_confidence": avg_conf,
    }
