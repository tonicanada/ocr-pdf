# OCR PDF Microservice (Google Document AI + FastAPI)

Este microservicio permite enviar un PDF y recibir como respuesta el texto extraído mediante **Google Document AI OCR**.  
Se empaqueta en Docker y puede usarse fácilmente desde **n8n** u otros sistemas.

---

## 🚀 Requisitos

- Docker + Docker Compose
- Una cuenta de Google Cloud con **Document AI habilitado**
- Un **Processor ID** del tipo OCR en Document AI
- Un archivo de credenciales (Service Account Key JSON)

---

## 📂 Estructura del proyecto

```text
ocr-pdf/
 ├── app/
 │    └── main.py
 ├── requirements.txt
 ├── Dockerfile
 ├── docker-compose.yml
 ├── .env.example
 └── secrets/
      └── key.json   # <-- NO subir nunca a git
```

---

## ⚙️ Configuración

1. Copia `.env.example` a `.env`:

   cp .env.example .env

2. Edita el archivo `.env` con los valores de tu proyecto de Google Cloud:

   - `GCP_PROJECT_ID`: tu proyecto
   - `GCP_LOCATION`: `us` o `eu` según tu procesador
   - `GCP_PROCESSOR_ID`: ID de tu processor OCR
   - `GOOGLE_APPLICATION_CREDENTIALS`: por defecto `/secrets/key.json`

3. Guarda tu **Service Account Key JSON** en `./secrets/key.json`.  
   ⚠️ Este archivo **no debe subirse a GitHub**.

---

## ▶️ Levantar el servicio

   docker compose up -d

Esto levanta el servicio en `http://localhost:8080/ocr-pdf`, accesible **solo desde la VM** (no expuesto al mundo).

---

## 🧪 Probar el servicio

   curl -X POST "http://localhost:8080/ocr-pdf" \
     -F "file=@ejemplo.pdf"

Respuesta típica:

{
  "pages": 2,
  "raw_text_per_page": ["Texto página 1", "Texto página 2"],
  "raw_text": "Texto completo del documento",
  "avg_confidence": 0.87
}

---

## 🔗 Usar desde n8n

1. Crea un **HTTP Request Node** en n8n.  
2. Configura:

   - **Method**: `POST`
   - **URL**: `http://host.docker.internal:8080/ocr-pdf`
   - **Send Body as**: `Form-Data`
   - **Field Name**: `file`
   - **Type**: `File`
   - **Value**: `={{$binary.data}}`

3. Conecta este nodo a cualquier otro que consuma el JSON devuelto.

---

## 📌 Notas

- El microservicio usa siempre **Document AI OCR Processor**, incluso si el PDF tiene texto embebido.
- Si quieres ahorrar costes, en el futuro puedes añadir un paso previo con `pdfplumber` para evitar OCR en PDFs vectoriales.
- Este servicio **no expone el puerto 8080 públicamente**, solo es accesible dentro de la máquina host.

---
