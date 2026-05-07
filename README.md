# API Microsserviço GTI

## 1. Visão geral

Este projeto implementa uma API REST em Python com FastAPI para integração com modelo de linguagem, permitindo enviar contexto, pergunta e parâmetros de resposta para obter uma saída textual gerada por IA.

O objetivo principal é disponibilizar um serviço simples, padronizado e reutilizável para experimentos, protótipos e integrações acadêmicas envolvendo sistemas inteligentes.

## 2. Objetivo do sistema

- Expor um endpoint de integração com IA.
- Centralizar configuração de acesso ao provedor externo via variáveis de ambiente.
- Fornecer endpoint de status para monitoramento operacional.
- Permitir documentação técnica da API em formatos web e PDF.

## 3. Tecnologias utilizadas

- Python 3
- FastAPI
- Pydantic
- Requests
- Sphinx (documentação)
- sphinxcontrib-openapi (renderização OpenAPI no Sphinx)

## 5. Endpoints principais

- GET /: mensagem de boas-vindas.
- GET /status: verificação de saúde do serviço.
- POST /ia/integracao: envio de contexto e pergunta para geração de resposta por IA.

## 6. Requisitos

- Python 3.10 ou superior.
- Dependências Python instaladas.
- Credenciais do provedor configuradas por variáveis de ambiente.

## 7. Instalação e execução

1. Criar e ativar ambiente virtual.
2. Instalar dependências do projeto.
3. Definir variáveis de ambiente.
4. Executar a API com servidor ASGI.

Exemplo de execução com Uvicorn:

python -m uvicorn main:app --host 0.0.0.0 --port 8000

## 8. Variáveis de ambiente

- OPENROUTER_API_KEY: chave de autenticação do provedor.
- OPENROUTER_URL: URL de chamada do endpoint do provedor.
- MODEL_NAME: identificador do modelo utilizado.

## 9. Documentação da API

### 9.1 Swagger UI estático

A documentação web pode ser publicada via arquivo HTML estático em docs/index.html, consumindo a especificação OpenAPI em docs/openapi.public.yaml.

### 9.2 Sphinx

O projeto inclui estrutura Sphinx para geração de documentação acadêmica e técnica.

Geração de HTML:

sphinx-build -b html docs_sphinx/source docs_sphinx/_build/html

Geração de PDF:

sphinx-build -M latexpdf docs_sphinx/source docs_sphinx/_build
