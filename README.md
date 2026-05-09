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
- Dotenv

## 4. Arquitetura e estrutura do projeto

O projeto é estruturado de forma simples e modular, permitindo fácil manutenção e expansão.

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

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

## 8. Variáveis de ambiente

- OPENROUTER_API_KEY: chave de autenticação do provedor.
- OPENROUTER_URL: URL de chamada do endpoint do provedor.
- MODEL_NAME: identificador do modelo utilizado.

## 9. Como executar a API

Para executar a API, siga os passos abaixo:

1. Certifique-se de que as dependências estão instaladas e as variáveis de ambiente estão configuradas corretamente.
   - Variáveis necessárias:
     - `OPENROUTER_API_KEY`: chave de autenticação do provedor.
     - `OPENROUTER_URL`: URL do endpoint do provedor.
     - `MODEL_NAME`: identificador do modelo utilizado.

2. Inicie o servidor utilizando o comando abaixo:

    ```bash
    python -m uvicorn main:app --host 0.0.0.0 --port 8000
    ```

3. Acesse os endpoints disponíveis para testar a API:
   - `GET /`: Retorna uma mensagem de boas-vindas.
   - `GET /status`: Verifica o status operacional da API.
   - `POST /ia/integracao`: Envia contexto e pergunta para geração de resposta por IA.

4. Para testar o endpoint POST, envie uma requisição com o seguinte corpo JSON de exemplo:

    ```json
    {
      "contexto": "Exemplo de contexto",
      "pergunta": "Exemplo de pergunta",
      "objetivo": "Exemplo de objetivo",
      "formato_saida": "Texto simples",
      "limites": "Exemplo de limites"
    }
    ```

5. Certifique-se de que o servidor está rodando e utilize ferramentas como Postman, cURL ou a extensão do VScode Thunder Client para interagir com a API.

## 10. Como rodar a API em Docker?

### Passo 1: Criar arquivo `.env`

Na raiz do projeto, crie um arquivo `.env` com as variáveis de ambiente necessárias:

```env
OPENROUTER_API_KEY=sua-chave-de-api
OPENROUTER_URL=url-do-provedor
MODEL_NAME=nome-do-modelo
```

### Passo 2: Construir a imagem Docker

Execute o comando para construir a imagem:

```bash
docker build -t imagem-python-microsservico ./
```

### Passo 3: Executar o container

Use o arquivo `.env` para passar as variáveis ao container:

```bash
docker run --env-file .env -d --name python-microsservico-container -p 8000:8000 imagem-python-microsservico
```

### Passo 4: Testar a API

A API estará disponível em `http://localhost:8000`. Você pode:

- Acessar a documentação interativa: `http://localhost:8000/docs`
- Testar o endpoint de status: `curl http://localhost:8000/status`

### Parar o container

```bash
docker stop api-microsservico-gti
```

## 11. Documentação da API

### 11.1 Swagger UI estático

A documentação web pode ser publicada via arquivo HTML estático em docs/index.html, consumindo a especificação OpenAPI em docs/openapi.public.yaml.

### 11.2 Sphinx

O projeto inclui estrutura Sphinx para geração de documentação acadêmica e técnica.

Geração de HTML:

```bash
sphinx-build -b html docs_sphinx/source docs_sphinx/_build/html
```

Geração de PDF:

```bash
sphinx-build -M latexpdf docs_sphinx/source docs_sphinx/_build
```
