from fastapi import HTTPException, status
from sqlmodel import select
from app.db import SessionDep
from app.models import Categoria, CategoriaCreate, CategoriaUpdate

class CategoriaService:
    def create_categoria(self, data: CategoriaCreate, session: SessionDep):
        categoria = Categoria.model_validate(data.model_dump())
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        return categoria

    def get_categoria(self, categoria_id: int, session: SessionDep):
        categoria = session.get(Categoria, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        return categoria

    def update_categoria(self, categoria_id: int, data: CategoriaUpdate, session: SessionDep):
        categoria = session.get(Categoria, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        update_data = data.model_dump(exclude_unset=True)
        categoria.sqlmodel_update(update_data)
        session.add(categoria)
        session.commit()
        session.refresh(categoria)
        return categoria

    def delete_categoria(self, categoria_id: int, session: SessionDep):
        categoria = session.get(Categoria, categoria_id)
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        session.delete(categoria)
        session.commit()
        return {"detail": "Categoría eliminada"}

    def get_all(self, session: SessionDep):
        return session.exec(select(Categoria)).all()
