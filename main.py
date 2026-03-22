import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="API de Implantacao de IA",
    description="Uma API para gerenciar a implantação de modelos de IA",
    version="1.0.0"
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "stepfun/step-3.5-flash:free"

class IntegracaoEntrada(BaseModel):
    texto: str

@app.post("/ia/integracao")
def integrar_ia(entrada: IntegracaoEntrada):
    if not OPENROUTER_API_KEY or not OPENROUTER_URL:
        raise HTTPException(status_code=500, detail="Cliente da API não configurado corretamente.")
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": entrada.texto}
        ],
    }
    
    try:
        req = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        req.raise_for_status()
        resposta = req.json()["choices"][0]["message"]["content"]
        return {"resposta": resposta}
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Erro ao integrar com a API: {e}")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Implantação de IA!"}

@app.get("/status")
def get_status():
    return {"status": "API está funcionando corretamente."}
