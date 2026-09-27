# PROXIER® — Backend

Backend da aplicação **PROXIER®**, desenvolvido em Python utilizando **Flask** e responsável pela disponibilização da API REST utilizada pelo frontend do projeto.

A API realiza o cadastro e consulta de usuários, gerenciamento da lista de cartas, exclusão de cartas e integração com o serviço externo **ViaCEP** para consulta de endereços a partir de um CEP.

A aplicação também disponibiliza documentação interativa da API por meio do **OpenAPI/Swagger**.

---

## Tecnologias utilizadas

* **Python**
* **Flask**
* **Flask-OpenAPI3**
* **Flask-CORS**
* **SQLAlchemy**
* **Requests**
* **OpenAPI / Swagger**
* **Docker**

---

## Funcionalidades

A API disponibiliza as seguintes funcionalidades:

* Cadastro de usuários;
* Login e validação de usuários cadastrados;
* Inclusão de cartas na lista de impressão;
* Consulta da lista de cartas de um usuário;
* Exclusão de uma carta da lista;
* Exclusão de todas as cartas de um usuário;
* Consulta de endereço por CEP;
* Documentação automática das rotas por OpenAPI/Swagger;
* Comunicação com o frontend por meio de API REST.

---

## Arquitetura do projeto

<img width="1751" height="929" alt="PUCSprint4-Arquitetura png" src="https://github.com/user-attachments/assets/f3909e3d-82c1-42d5-b86e-4620c9913fb3" />

## Estrutura esperada do projeto

A estrutura básica do backend deve conter os seguintes arquivos:

```text
PROXIER-BACKEND/
├── database
├── model/
|   └──__init__.py
|   └──base.py
|   └──lista.py
|   └──usuario.py
├── schemas/
|   └──__init__.py
|   └──error.py
|   └──lista.py
|   └──usuarios.py
├── venv/...
├── app.py
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# Instalação

## Pré-requisitos

Para executar o projeto localmente, é necessário possuir:

* **Python 3**;
* **pip**;
* **Docker**;
* **Git**, caso o projeto seja obtido por meio de um repositório.

---

## 1. Clonar o projeto

Caso o projeto esteja hospedado em um repositório Git:

```bash
git clone <URL_DO_REPOSITORIO>
```

Entre no diretório do backend:

```bash
cd PROXIER-BACKEND
```

---

## 2. Criar um ambiente virtual

Recomenda-se utilizar um ambiente virtual para isolar as dependências do projeto.

### Windows

```bash
python -m venv venv
```

Ative o ambiente:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Ative o ambiente:

```bash
source venv/bin/activate
```

---

## 3. Instalar as dependências

Com o ambiente virtual ativado, instale as dependências:

```bash
pip install -r requirements.txt
```

O arquivo `requirements.txt` contém as dependências e respectivas versões utilizadas pelo projeto.

---

# Execução local

Após instalar as dependências, execute a aplicação Python.

Caso o projeto utilize diretamente o arquivo `app.py`:

```bash
flask run -p 3000 -h 0.0.0.0
```

A API deverá ser disponibilizada conforme a configuração do servidor Flask.

---

# Execução com Docker

A aplicação pode ser executada de forma conteinerizada utilizando Docker.
As seguintes instruções leva em consideração que o usuário já contém o **Docker** instalado e funcionando em sua máquina.

## 1. Construir a imagem

Na raiz do projeto, onde estiver localizado o `Dockerfile`, execute:

```bash
docker build -t proxier-backend .
```

---

## 2. Executar o container

Após a criação da imagem:

```bash
docker run -d -p 3000:3000 proxier-backend
```

A API poderá então ser acessada em:

```text
http://localhost:3000
```

> **Importante:** Sempre utilize a porta `3000` para ativação do backend, visto que o frontend da aplicaçãõ consulta as rotas a partir desta rota.

---

## 3. Parar o container

```bash
docker stop proxier-backend
```

Para remover o container:

```bash
docker rm proxier-backend
```

---

# Documentação da API

O backend utiliza `flask-openapi3` para disponibilizar a documentação da API.

A rota principal:

```http
GET /
```

redireciona para:

```text
/openapi
```

Portanto, após iniciar o backend, a documentação pode ser acessada em:

```text
http://localhost:3000/
```

ou diretamente em:

```text
http://localhost:3000/openapi
```

A documentação permite visualizar as rotas disponíveis, parâmetros, schemas e operações da API.

---

# Rotas da API

## Usuários / Login

### Cadastrar usuário

```http
POST /usuario
```

Cadastra um novo usuário no banco de dados.

### Corpo da requisição

```json
{
    "nome": "Joao",
    "cpf": "12345678900",
    "email": "joao@email.com"
}
```

### Respostas

**Sucesso:**

```text
201 Created
```

**Usuário já cadastrado:**

```text
400 Bad Request
```

**Erro interno:**

```text
500 Internal Server Error
```

---

## Consultar usuário / Login

```http
GET /usuario?nome={nome}
```

Verifica se existe um usuário cadastrado com o nome informado.

### Exemplo

```text
GET /usuario?nome=Joao
```

### Respostas

Quando o usuário existe:

```json
{
    "nome": "Joao"
}
```

Usuário não encontrado:

```text
400 Bad Request
```

---

# Lista de Cartas

## Consultar cartas do usuário

```http
GET /cartas?nome={nome}
```

Retorna as cartas cadastradas na lista de impressão do usuário.

### Exemplo

```text
GET /cartas?nome=Joao
```

### Exemplo de resposta

```json
{
    "lista": [
        {
            "carta": "Transportador de Pacotes",
            "quantidade": 2
        },
        {
            "carta": "Legião Inabalável",
            "quantidade": 1
        }
    ]
}
```

As quantidades das cartas são agrupadas pelo nome da carta.

---

## Adicionar carta

```http
POST /carta
```

Adiciona uma carta à lista de impressão de um usuário.

### Corpo da requisição

```json
{
    "usuario": "Joao",
    "carta": "Transportador de Pacotes",
    "quantidade": 2
}
```

A API valida se o usuário existe e se a quantidade informada é maior que zero.

### Respostas

```text
201 Created
400 Bad Request
500 Internal Server Error
```

---

## Remover carta

```http
DELETE /cartas
```

Remove da lista do usuário todas as ocorrências da carta informada.

### Corpo da requisição

```json
{
    "usuario": "Joao",
    "carta": "Transportador de Pacotes"
}
```

A API verifica:

1. Se o usuário existe;
2. Se a carta está presente na lista;
3. Remove os registros correspondentes.

---

## Remover todas as cartas do usuário

```http
DELETE /cartasdousuario?usuario={usuario}
```

Remove todas as cartas pertencentes ao usuário informado.

### Exemplo

```text
DELETE /cartasdousuario?usuario=Joao
```

Essa operação é utilizada pelo frontend após a solicitação de envio da lista.

---

# Busca de CEP - API externa VIACEP

## Consultar endereço

```http
GET /buscacep?cep={cep}
```

Consulta um CEP e retorna os dados de endereço necessários para o preenchimento do formulário de envio.

Antes de realizar a consulta externa, a API verifica se o CEP:

* possui exatamente 8 caracteres;
* contém somente números.

### Exemplo

```text
GET /buscacep?cep=20040020
```

A API utiliza o serviço externo **ViaCEP** para realizar a consulta. Em sesguida, ela trata as informações para retornanr somente o necessário para o projeto.

O endereço consultado é:

```text
http://viacep.com.br/ws/{cep}/json/
```

### Exemplo de resposta

```json
{
    "bairro": "Centro",
    "cidade": "Rio de Janeiro",
    "estado": "Rio de Janeiro",
    "estadouf": "RJ",
    "rua": "Avenida Exemplo"
}
```

---


# Integração externa - API Via CEP

A rota `/buscacep` utiliza um serviço externo para obter informações de endereço.
Essa integração é realizada utilizando a biblioteca `requests`.

---
