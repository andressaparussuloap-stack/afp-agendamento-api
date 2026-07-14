from fastapi import FastAPI
from app.api.routes import empresas
from app.api.routes import clientes
from app.api.routes import servicos
from app.api.routes import agendamentos
from app.api.routes import auth

app = FastAPI(
    title="AFP Agendamento API"
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


