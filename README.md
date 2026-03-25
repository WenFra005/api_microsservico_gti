# API Microsservico GTI

## 1. Visao geral
Este projeto implementa uma API REST em Python com FastAPI para integracao com modelo de linguagem, permitindo enviar contexto, pergunta e parametros de resposta para obter uma saida textual gerada por IA.

O objetivo principal e disponibilizar um servico simples, padronizado e reutilizavel para experimentos, prototipos e integracoes academicas envolvendo sistemas inteligentes.

## 2. Objetivo do sistema
- Expor um endpoint de integracao com IA.
- Centralizar configuracao de acesso ao provedor externo via variaveis de ambiente.
- Fornecer endpoint de status para monitoramento operacional.
- Permitir documentacao tecnica da API em formatos web e PDF.

## 3. Tecnologias utilizadas
- Python 3
- FastAPI
- Pydantic
- Requests
- Sphinx (documentacao)
- sphinxcontrib-openapi (renderizacao OpenAPI no Sphinx)

## 5. Endpoints principais
- GET /: mensagem de boas-vindas.
- GET /status: verificacao de saude do servico.
- POST /ia/integracao: envio de contexto e pergunta para geracao de resposta por IA.

## 6. Requisitos
- Python 3.10 ou superior.
- Dependencias Python instaladas.
- Credenciais do provedor configuradas por variaveis de ambiente.

## 7. Instalacao e execucao
1. Criar e ativar ambiente virtual.
2. Instalar dependencias do projeto.
3. Definir variaveis de ambiente.
4. Executar a API com servidor ASGI.

Exemplo de execucao com Uvicorn:

uvicorn main:app --reload

## 8. Variaveis de ambiente
- OPENROUTER_API_KEY: chave de autenticacao do provedor.
- OPENROUTER_URL: URL de chamada do endpoint do provedor.
- MODEL_NAME: identificador do modelo utilizado.

## 9. Documentacao da API
### 9.1 Swagger UI estatico
A documentacao web pode ser publicada via arquivo HTML estatico em docs/index.html, consumindo a especificacao OpenAPI em docs/openapi.public.yaml.

### 9.2 Sphinx
O projeto inclui estrutura Sphinx para geracao de documentacao academica e tecnica.

Geracao de HTML:

sphinx-build -b html docs_sphinx/source docs_sphinx/_build/html

Geracao de PDF:

sphinx-build -M latexpdf docs_sphinx/source docs_sphinx/_build
