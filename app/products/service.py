from fastapi import HTTPException, status
from sqlmodel import select
from app.db import SessionDep
from app.models import Product, ProductCreate, ProductUpdate


class ProductService:
    # CREATE
    # ----------------------
    def create_product(self, product_data: ProductCreate, session: SessionDep):
        product_db = Product.model_validate(product_data.model_dump())
        session.add(product_db)
        session.commit()
        session.refresh(product_db)
        return product_db

    # GET ONE
    # ----------------------
    def read_product(self, product_id: int, session: SessionDep):
        product_db = session.get(Product, product_id)
        if not product_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )
        return product_db

    # UPDATE
    # ----------------------
    def update_product(self, product_id: int, product_data: ProductUpdate, session: SessionDep):
        product_db = session.get(Product, product_id)
        if not product_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )
        product_data_dict = product_data.model_dump(exclude_unset=True)
        product_db.sqlmodel_update(product_data_dict)
        session.add(product_db)
        session.commit()
        session.refresh(product_db)
        return product_db

    # GET ALL
    # ----------------------
    def get_all_products(self, session: SessionDep):
        return session.exec(select(Product)).all()

    # DELETE
    # ----------------------
    def delete_product(self, product_id: int, session: SessionDep):
        product_db = session.get(Product, product_id)
        if not product_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )
        session.delete(product_db)
        session.commit()
        return {"detail": "Producto eliminado correctamente"}
