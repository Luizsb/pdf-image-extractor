# 🖼️ PDF Image Extractor

Aplicação web moderna para extrair imagens de arquivos PDF de forma rápida e intuitiva.

## ✨ Funcionalidades

- 📄 Upload de PDF por drag & drop ou seleção de arquivo
- 🎨 Visualização de imagens organizadas por página
- ✅ Seleção múltipla de imagens
- 📦 Download individual ou em lote (ZIP)
- 🚀 Interface moderna e responsiva com React
- ⚡ Processamento rápido com FastAPI

## 🛠️ Tecnologias

### Frontend
- React 18
- Vite
- TailwindCSS
- Axios
- React Dropzone
- Framer Motion

### Backend
- Python 3.8+
- FastAPI
- PyMuPDF (fitz)
- Uvicorn

## 🚀 Como Usar

### Pré-requisitos

- Python 3.8 ou superior
- Node.js 16 ou superior
- npm ou yarn

### Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/Luizsb/pdf-image-extractor.git
cd pdf-image-extractor
```

2. **Configure o Backend**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac

pip install fastapi uvicorn pymupdf python-multipart
```

3. **Configure o Frontend**
```bash
cd frontend
npm install
```

### Executar o Projeto

1. **Inicie o Backend** (Terminal 1)
```bash
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

2. **Inicie o Frontend** (Terminal 2)
```bash
cd frontend
npm run dev
```

3. **Acesse a aplicação**
```
http://localhost:5173
```

## 📖 Como Usar a Aplicação

1. Arraste e solte um PDF ou clique para selecionar
2. Aguarde a extração das imagens
3. Visualize as imagens organizadas por página
4. Selecione as imagens desejadas (opcional)
5. Baixe individualmente ou em ZIP

## 📦 Estrutura do Projeto

```
pdf-image-extractor/
├── backend/
│   ├── main.py              # API FastAPI
│   ├── requirements.txt     # Dependências Python
│   └── venv/               # Ambiente virtual
├── frontend/
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── App.jsx         # Componente principal
│   │   └── index.css       # Estilos globais
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🎨 Features

- ✅ Extração de imagens em PNG, JPG, JPEG
- ✅ Suporte para PDFs com CMYK, RGB e Grayscale
- ✅ Download otimizado (sem compressão redundante)
- ✅ Interface responsiva (mobile-friendly)
- ✅ Feedback visual durante processamento
- ✅ Organização por páginas do PDF

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

## 📄 Licença

MIT License - sinta-se livre para usar em seus projetos!

## 👨‍💻 Autor

Desenvolvido com ❤️ por [Luizsb](https://github.com/Luizsb)

---

⭐ Se este projeto foi útil, considere dar uma estrela!

