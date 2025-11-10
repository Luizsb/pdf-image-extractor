from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List
import fitz  # PyMuPDF
from io import BytesIO
import zipfile
import base64
import sys
import io
import os

# Configurar encoding UTF-8 para evitar erros no Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

app = FastAPI()

# CORS - permitir que o frontend acesse o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/extract")
async def extract_images(file: UploadFile = File(...)):
    """Extrai todas as imagens de um PDF"""
    print(f"\n========== INICIANDO EXTRAÇÃO ==========")
    print(f"Arquivo: {file.filename}")
    
    try:
        pdf_bytes = await file.read()
        print(f"Tamanho: {len(pdf_bytes)} bytes")
        images_data = []
        
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        print(f"PDF aberto: {len(doc)} páginas")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            image_list = page.get_images(full=True)
            print(f"Página {page_num + 1}: {len(image_list)} imagens")
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    
                    # Método 1: Extrair diretamente (preserva JPG original)
                    try:
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        ext = base_image["ext"]
                        
                        # Se já é JPG, usar diretamente (MUITO mais rápido)
                        if ext in ["jpeg", "jpg"]:
                            img_base64 = base64.b64encode(image_bytes).decode("utf-8")
                            images_data.append({
                                "name": f"pagina_{page_num + 1:03d}_img_{img_index + 1:02d}.jpg",
                                "data": f"data:image/jpeg;base64,{img_base64}",
                                "page": page_num + 1
                            })
                            print(f"    OK - JPG direto (rápido)")
                            continue
                    except:
                        pass
                    
                    # Método 2: Converter usando Pixmap
                    pix = fitz.Pixmap(doc, xref)
                    
                    # Garantir que está em RGB
                    if pix.n - pix.alpha > 3:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    if pix.alpha:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    
                    # Redimensionar se muito grande (max 1200px)
                    max_dim = 1200
                    if pix.width > max_dim or pix.height > max_dim:
                        scale = max_dim / max(pix.width, pix.height)
                        mat = fitz.Matrix(scale, scale)
                        pix_small = fitz.Pixmap(pix, 0, pix.irect, mat)
                        pix = pix_small
                    
                    # Usar JPEG qualidade 85 (5-10x menor que PNG)
                    img_data = pix.tobytes("jpeg", jpg_quality=85)
                    img_base64 = base64.b64encode(img_data).decode("utf-8")
                    
                    images_data.append({
                        "name": f"pagina_{page_num + 1:03d}_img_{img_index + 1:02d}.jpg",
                        "data": f"data:image/jpeg;base64,{img_base64}",
                        "page": page_num + 1
                    })
                    print(f"    OK - Convertido para JPEG")
                    
                    pix = None
                    
                except Exception as img_error:
                    print(f"    ERRO: {str(img_error)}")
                    import traceback
                    traceback.print_exc()
                    continue
        
        doc.close()
        
        print(f"Total de imagens extraídas: {len(images_data)}")
        print(f"========== FIM DA EXTRAÇÃO ==========\n")
        
        if len(images_data) == 0:
            return JSONResponse(
                status_code=400,
                content={"detail": "Nenhuma imagem encontrada no PDF"}
            )
        
        return {"images": images_data}
    
    except Exception as e:
        print(f"ERRO CRÍTICO: {str(e)}")
        import traceback
        traceback.print_exc()
        print(f"========================================\n")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Erro ao processar PDF: {str(e)}"}
        )

@app.post("/download-zip")
async def download_zip(files: List[str]):
    """Cria um ZIP com as imagens selecionadas - OTIMIZADO"""
    try:
        zip_buffer = BytesIO()
        
        # Usar compressão mais rápida (ZIP_STORED = sem compressão, mais rápido)
        # Imagens PNG já são comprimidas, então não adianta comprimir novamente
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

# Servir frontend estático (se existir)
if os.path.exists("./frontend/dist"):
    app.mount("/", StaticFiles(directory="./frontend/dist", html=True), name="frontend")
