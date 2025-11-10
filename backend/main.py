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

@app.get("/")
def read_root():
    return {"status": "Backend funcionando!"}

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
                    pix = fitz.Pixmap(doc, xref)
                    print(f"  Imagem {img_index + 1}: n={pix.n}, alpha={pix.alpha}, width={pix.width}, height={pix.height}")
                    
                    # Garantir que está em RGB ou Grayscale
                    if pix.n - pix.alpha > 3:  # CMYK ou outro espaço de cor
                        print(f"    Convertendo de CMYK/outro para RGB")
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    
                    # Se tem alpha, remover
                    if pix.alpha:
                        print(f"    Removendo canal alpha")
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    
                    # Converter para PNG
                    img_data = pix.tobytes("png")
                    img_base64 = base64.b64encode(img_data).decode("utf-8")
                    
                    images_data.append({
                        "name": f"pagina_{page_num + 1:03d}_img_{img_index + 1:02d}.png",
                        "data": f"data:image/png;base64,{img_base64}",
                        "page": page_num + 1
                    })
                    print(f"    OK - Imagem extraída com sucesso")
                    
                    pix = None  # Liberar memória
                    
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
