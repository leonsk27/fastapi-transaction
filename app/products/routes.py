from fastapi import APIRouter, status
from app.db import SessionDep
from app.models import Product, ProductCreate, ProductUpdate
from app.products.service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])
service = ProductService()


# CREATE
# ----------------------
@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate, session: SessionDep):
    return service.create_product(product_data, session)


# GET ONE
# ----------------------
@router.get("/{product_id}", response_model=Product)
async def read_product(product_id: int, session: SessionDep):
    return service.read_product(product_id, session)


# UPDATE
# ----------------------
@router.patch("/{product_id}", response_model=Product, status_code=status.HTTP_200_OK)
async def update_product(product_id: int, product_data: ProductUpdate, session: SessionDep):
    return service.update_product(product_id, product_data, session)


# GET ALL
# ----------------------
@router.get("/", response_model=list[Product])
async def get_all_products(session: SessionDep):
    return service.get_all_products(session)


# DELETE
# ----------------------
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, session: SessionDep):
    return service.delete_product(product_id, session)
