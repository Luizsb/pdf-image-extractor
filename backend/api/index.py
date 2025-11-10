from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Adicionar o diretório backend ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app

# Esta é a aplicação que o Vercel vai usar
app = app

