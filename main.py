from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from urllib import request, error
import json

app = FastAPI(
    title="API de Implantacao de IA",
    description="Uma API para gerenciar a implantação de modelos de IA",
    version="1.0.0"
)

class IntegracaoEntrada(BaseModel):
    texto: str

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API de Implantação de IA!"}

@app.get("/status")
def get_status():
    return {"status": "API está funcionando corretamente."}
