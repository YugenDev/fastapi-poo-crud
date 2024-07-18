from fastapi import FastAPI
from api.usuario_api import router as usuario_router
from api.registro_emocional_api import router as registro_emocional_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers para cada modelo
app.include_router(customer.router, prefix="/customers", tags=["customers"])
