import os

from fastapi import FastAPI, HTTPException
from openai import OpenAI
from pydantic import BaseModel
from urllib import request, error
import json

app = FastAPI(
    title="API de Implantacao de IA",
    description="Uma API para gerenciar a implantação de modelos de IA",
    version="1.0.0"
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_API_URL")
MODEL_NAME = "stepfun/step-3.5-flash:free"

client = OpenAI(
    base_url=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
) 

class IntegracaoEntrada(BaseModel):
    texto: str

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Implantação de IA!"}

@app.get("/status")
def get_status():
    return {"status": "API está funcionando corretamente."}
