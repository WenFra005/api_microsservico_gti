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
if OPENROUTER_API_KEY is None or OPENROUTER_BASE_URL is None:
    client = None
else:
    client = OpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=OPENROUTER_API_KEY,
    )

class IntegracaoEntrada(BaseModel):
    texto: str

@app.post("/ia/integracao")
def integrar_ia(entrada: IntegracaoEntrada):
    if client is None:
        raise HTTPException(status_code=500, detail="Cliente da API não configurado corretamente.")
    try:
        resposta = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": entrada.texto}]
        )
        return {"resposta": resposta.choices[0].message.content}
    except error.HTTPError as e:
        raise HTTPException(status_code=502, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Implantação de IA!"}

@app.get("/status")
def get_status():
    return {"status": "API está funcionando corretamente."}
