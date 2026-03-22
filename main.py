import os

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="API de Implantacao de IA",
    description="Uma API para gerenciar a implantação de modelos de IA",
    version="1.0.0",
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "stepfun/step-3.5-flash:free"


class IntegracaoEntrada(BaseModel):
    contexto: str = Field(..., description="Contexto do problema ou tarefa para a IA")
    pergunta: str = Field(..., description="Pergunta principal para a IA responder")
    objetivo: str = Field(
        default="Fornecer uma resposta útil e presisa com clareza e objetividade."
    )
    formato_saida: str = Field(default="Texto simples")
    limites: str = Field(
        default="Evitar respostas vagas ou genéricas, e não fornecer informações falsas ou enganosas."
    )


@app.post("/ia/integracao")
def integrar_ia(entrada: IntegracaoEntrada):
    if not OPENROUTER_API_KEY or not OPENROUTER_URL:
        raise HTTPException(
            status_code=500, detail="Cliente da API não configurado corretamente."
        )
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": f"Você é um assistente de IA especializado em {entrada.objetivo}",
            },
            {"role": "user", "content": f"Contexto: {entrada.contexto}"},
            {"role": "user", "content": f"Pergunta: {entrada.pergunta}"},
            {
                "role": "user",
                "content": f"Formato de saída desejado: {entrada.formato_saida}",
            },
            {"role": "system", "content": f"Limites: {entrada.limites}"},
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
