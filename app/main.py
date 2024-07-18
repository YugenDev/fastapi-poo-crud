from fastapi import FastAPI
from crud.customer import router as customer_router
from crud.employee import router as employee_router
from crud.product import router as product_router
#from crud.sale import router as sale_router
from crud.category import router as category_router
from database.database import engine, Base
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
app.include_router(customer_router, prefix="/employees", tags=["employees"])
app.include_router(product_router, prefix="/products", tags=["products"])
#app.include_router(sale_router, prefix="/sales", tags=["sales"])
app.include_router(category_router, prefix="/categories", tags=["categories"])
