import os

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from requests import RequestException, Timeout

app = FastAPI(
    title="API de Implantacao de IA",
    description="Uma API para gerenciar a implantação de modelos de IA",
    version="1.0.0",
)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = os.getenv("OPENROUTER_URL")
MODEL_NAME = os.getenv("MODEL_NAME")


class IntegracaoEntrada(BaseModel):
    """Payload de entrada para integração com IA.

    Define os campos necessários para gerar uma resposta contextualizada no modelo configurado.
    """

    contexto: str = Field(
        default="Contexto padrão",
        description="Contexto do problema ou tarefa para a IA",
    )
    pergunta: str = Field(
        default="Pergunta padrão",
        description="Pergunta principal para a IA responder",
    )
    objetivo: str = Field(
        default="Fornecer uma resposta útil e presisa com clareza e objetividade."
    )
    formato_saida: str = Field(default="Texto simples")
    limites: str = Field(
        default="Evitar respostas vagas ou genéricas e informações falsas ou enganosas."
    )


@app.post(
    "/ia/integracao",
    responses={
        200: {
            "description": "Resposta gerada pela IA",
            "content": {
                "application/json": {
                    "example": {"detail": "Resposta gerada pela IA"}
                }
            },
        },
        422: {
            "description": "Erro de validação da requisição",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Erro de validação: campo 'pergunta' é obrigatório."
                    }
                }
            },
        },
        500: {
            "description": "Erro interno do servidor",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Cliente da API não configurado corretamente."
                    }
                }
            },
        },
        502: {
            "description": "Falha na comunicação com o OpenRouter",
            "content": {
                "application/json": {
                    "example": {"detail": "Falha na chamada ao OpenRouter."}
                }
            },
        },
        504: {
            "description": "Timeout ao chamar o OpenRouter",
            "content": {
                "application/json": {
                    "example": {"detail": "Timeout ao chamar o OpenRouter."}
                }
            },
        },
    },
)
def integrar_ia(entrada: IntegracaoEntrada):
    """Gera uma resposta de IA com base no contexto e na pergunta informados.

    Este endpoint envia a solicitação ao provedor configurado e retorna o texto gerado.
    """

    if not OPENROUTER_API_KEY or not OPENROUTER_URL:
        raise HTTPException(
            status_code=500,
            detail="Cliente da API não configurado corretamente.",
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
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=(5, 30),
        )
        response.raise_for_status()

    except Timeout as e:
        raise HTTPException(
            status_code=504,
            detail="Timeout ao chamar o OpenRouter. Erro: " + str(e),
        )

    except RequestException as e:
        raise HTTPException(
            status_code=502,
            detail="Falha na chamada ao OpenRouter. Erro: " + str(e),
        )

    resposta = response.json()["choices"][0]["message"]["content"]
    return {"resposta": resposta}


@app.get("/")
def read_root():
    """Retorna mensagem de boas-vindas da API.

    Útil para validação rápida de disponibilidade do serviço.
    """
    return {"message": "Bem-vindo à API de Implantação de IA!"}


@app.get("/status")
def get_status():
    """Retorna o status operacional da API.

    Endpoint de health-check para monitoramento e integração com orquestradores.
    """
    return {"status": "API está funcionando corretamente."}
