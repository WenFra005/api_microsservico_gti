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
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "stepfun/step-3.5-flash:free"


class IntegracaoEntrada(BaseModel):
    """A classe `IntegracaoEntrada` é um modelo de dados que define a estrutura da entrada esperada
    para a função de integração com a IA. Ela herda de `BaseModel` do Pydantic, o que permite a
    validação automática dos dados de entrada.

    Args:
        BaseModel (class): A classe base para modelos de dados no Pydantic, que fornece
        funcionalidades de validação e serialização.
    """

    contexto: str = Field(
        ..., description="Contexto do problema ou tarefa para a IA"
    )
    pergunta: str = Field(
        ..., description="Pergunta principal para a IA responder"
    )
    objetivo: str = Field(
        default="Fornecer uma resposta útil e presisa com clareza e objetividade."
    )
    formato_saida: str = Field(default="Texto simples")
    limites: str = Field(
        default="Evitar respostas vagas ou genéricas e informações falsas ou enganosas."
    )


@app.post("/ia/integracao")
def integrar_ia(entrada: IntegracaoEntrada):
    """A função `integrar_ia` é um endpoint de API que recebe uma solicitação POST contendo um
    objeto `IntegracaoEntrada`. Ele utiliza as informações fornecidas para fazer uma solicitação à
    API do OpenRouter, enviando o contexto, a pergunta, o objetivo, o formato de saída desejado e
    os limites para a IA. A resposta da IA é então retornada ao cliente.

    Args:
        entrada (IntegracaoEntrada): Um objeto que contém o contexto, a pergunta, o objetivo, o
        formato de saída desejado e os limites para a IA.

    Raises:
        HTTPException: Se as variáveis de ambiente para a chave da API ou a URL do OpenRouter não
        estiverem configuradas corretamente, ou se houver um erro ao fazer a solicitação à API do
        OpenRouter, uma exceção HTTP será levantada com um status code 500 e uma mensagem de
        detalhe apropriada.
        HTTPException: Se houver um erro ao fazer a solicitação à API do OpenRouter, uma exceção
        HTTP será levantada com um status code 500 e uma mensagem de detalhe apropriada.

    Returns:
        dict: Um dicionário contendo a resposta da IA, com a chave "resposta" e o valor sendo a
        resposta gerada pela IA.
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
    """Endpoint para a rota raiz da API.

    Returns:
        dict: Uma mensagem de boas-vindas à API.
    """
    return {"message": "Bem-vindo à API de Implantação de IA!"}


@app.get("/status")
def get_status():
    """Endpoint para verificar o status da API.

    Returns:
        dict: Um dicionário indicando que a API está funcionando corretamente.
    """
    return {"status": "API está funcionando corretamente."}
