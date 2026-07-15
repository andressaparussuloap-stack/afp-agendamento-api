from fastapi import FastAPI
from app.api.routes import empresas
from app.api.routes import clientes
from app.api.routes import servicos
from app.api.routes import agendamentos
from app.api.routes import auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AFP Agendamento API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(empresas.router)
app.include_router(clientes.router)
app.include_router(servicos.router)
app.include_router(agendamentos.router)
app.include_router(auth.router)


@app.get("/")
def home():
    return {
        "status": "API funcionando",
        "projeto": "AFP Agendamento"
    }


