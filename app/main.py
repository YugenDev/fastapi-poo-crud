from fastapi import FastAPI
from crud.customer import router as customer_router
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers para cada modelo
app.include_router(customer_router, prefix="/customers", tags=["customers"])
