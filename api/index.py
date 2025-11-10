from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from typing import List
import fitz
from io import BytesIO
import zipfile
import base64
import sys
import io

# Configurar encoding UTF-8 para evitar erros no Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
def read_root():
    return {"status": "Backend funcionando!"}

@app.post("/api/extract")
async def extract_images(file: UploadFile = File(...)):
    """Extrai todas as imagens de um PDF"""
    pdf_bytes = await file.read()
    images_data = []
    
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    
                    # Garantir que está em RGB
                    if pix.n - pix.alpha > 3:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    
                    # Se tem alpha, remover
                    if pix.alpha:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    
                    # Converter para PNG
                    img_data = pix.tobytes("png")
                    img_base64 = base64.b64encode(img_data).decode("utf-8")
                    
                    images_data.append({
                        "name": f"pagina_{page_num + 1:03d}_img_{img_index + 1:02d}.png",
                        "data": f"data:image/png;base64,{img_base64}",
                        "page": page_num + 1
                    })
                    
                    pix = None
                    
                except Exception:
                    continue
        
        doc.close()
        
        if len(images_data) == 0:
            return JSONResponse(
                status_code=400,
                content={"detail": "Nenhuma imagem encontrada no PDF"}
            )
        
        return {"images": images_data}
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Erro ao processar PDF: {str(e)}"}
        )

@app.post("/api/download-zip")
async def download_zip(files: List[str]):
    """Cria um ZIP com as imagens selecionadas"""
    try:
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_STORED) as zip_file:
            for file_data in files:
                name, base64_data = file_data.split("|", 1)
                image_bytes = base64.b64decode(base64_data)
                zip_file.writestr(name, image_bytes)
        
        zip_buffer.seek(0)
        
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={
                "Content-Disposition": "attachment; filename=imagens.zip",
                "Cache-Control": "no-cache"
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"Erro ao criar ZIP: {str(e)}"}
        )

# Para o Vercel
handler = app

