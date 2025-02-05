from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from .db import init_db
from .routers import customers, plans, transactions

version = "v1"

description = """
A REST API for a book review web service.

This REST API is able to;
- Create Read Update And delete books
- Add reviews to books
- Add tags to Books e.t.c.
    """

version_prefix =f"/api/{version}"

app = FastAPI(
    lifespan=init_db,
    #lifespan=life_spna,
    title="AppTransactionFastAPI",
    description="API de un Sistema de transacción, usando FastApi con Python",
    version="0.0.1",
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
    contact={
        "name": "Henry Alejandro Taby Zenteno",
        "url": "https://github.com/henrytaby",
        "email": "henry.taby@gmail.com",
    },
    #openapi_url=f"{version_prefix}/openapi.json",
    #docs_url=f"{version_prefix}/docs",
    #redoc_url=f"{version_prefix}/redoc",
    openapi_tags=[
        {
            "name": "Customers",
            "description": "Funcionalidades que se tiene para realizar con el cliente (Customer)",
        },
        {
            "name": "Transactions",
            "description": "Todas las transacciones realizadas por el cliente (Customer)",
        },
        {
            "name": "Plans",
            "description": "Lista de planes relacionados al cliente (Customer)",
        },
    ],
)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(plans.router)

"""
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.url} completed in: {process_time:.4f} seconds")
    return response


@app.middleware("http") 
async def log_request_headers(request: Request, call_next):
    print("Request Headers:")
    for header, value in request.headers.items():
        print(f"{header}: {value}")
    response = await call_next(request) 
    return response
"""

security = HTTPBasic()

@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)] ):
    print(credentials)
    if credentials.username == "admin" and credentials.password=="123":
        return {"message": f"Hola, Mundo {credentials.username}!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


"""
country_timezones = {
    "CO" : "America/Bogota",
    "MX" : "America/Mexico_City",
    "AR" : "America/Argentina/Buenos_Aires",
    "BR" : "America/Sao_Paulo",
    "PE" : "America/Lima",
}

@app.get('/time/{iso_code}')
async def get_time_by_iso(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    now = datetime.now(tz)
    #return {"datetime": now.strftime('%Y-%m-%d %H:%M:%S')}
    return {"datetime": now}



@app.post('/invoices')
async def create_invoice(invoice_data: Invoice):
    return invoice_data
"""
