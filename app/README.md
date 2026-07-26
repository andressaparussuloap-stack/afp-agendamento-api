# 🚀 AFP Agendamento API

API de gerenciamento de agendamentos desenvolvida com **FastAPI**, **PostgreSQL** e **SQLAlchemy**.

O projeto tem como objetivo criar uma solução de agendamento para empresas, permitindo cadastrar empresas, clientes, serviços e futuramente integrar atendimento automático via WhatsApp.

---

## 📌 Tecnologias utilizadas

* Python 3.10+
* FastAPI
* Uvicorn
* PostgreSQL
* SQLAlchemy
* Alembic (migrações do banco de dados)
* Pydantic
* Git e GitHub

---

## 🎯 Funcionalidades atuais

### 🏢 Empresas

✅ Criar empresa
✅ Listar empresas
✅ Buscar empresa por ID
✅ Atualizar empresa
✅ Excluir empresa

---

### 👥 Clientes

✅ Criar cliente
✅ Listar clientes
✅ Relacionar cliente com empresa

---

### ✂️ Serviços

✅ Cadastro de serviços
✅ Estrutura preparada para agendamentos

---

## 📂 Estrutura do projeto

```text
afp-agendamento-api
│
├── app
│   ├── api
│   │   └── routes
│   │       ├── empresas.py
│   │       ├── clientes.py
│   │       └── servicos.py
│   │
│   ├── database
│   │   └── database.py
│   │
│   ├── models
│   │   ├── empresa.py
│   │   ├── cliente.py
│   │   └── servico.py
│   │
│   ├── schemas
│   │   ├── empresa.py
│   │   ├── cliente.py
│   │   └── servico.py
│   │
│   └── main.py
│
├── alembic
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## ⚙️ Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/andressaparussuloap-stack/afp-agendamento-api.git
```

---

### 2. Criar ambiente virtual

```bash
python3 -m venv .venv
```

Ativar:

Linux:

```bash
source .venv/bin/activate
```

---

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 4. Configurar variáveis de ambiente

Criar arquivo `.env`:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/afp_agendamento

SECRET_KEY=sua_chave_secreta

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

### 5. Executar migrações

```bash
alembic upgrade head
```

---

### 6. Iniciar API

```bash
uvicorn app.main:app --reload
```

---

## 📚 Documentação da API

Após iniciar o projeto:

Swagger:

```
http://127.0.0.1:8000/docs
```

OpenAPI:

```
http://127.0.0.1:8000/openapi.json
```

---

## 🛠️ Próximos passos

* [ ] Sistema de agendamentos
* [ ] Autenticação com JWT
* [ ] Integração WhatsApp
* [ ] Dashboard administrativo
* [ ] Sistema multiempresas
* [ ] Deploy em produção

---

## 👩‍💻 Desenvolvedora

**Andressa Ferreira Parussulo**

Projeto desenvolvido para estudo, portfólio e evolução em desenvolvimento backend.

---

⭐ Projeto em evolução 🚀
