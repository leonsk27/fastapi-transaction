from fastapi import APIRouter, status
from app.db import SessionDep
from app.models import Categoria, CategoriaCreate, CategoriaUpdate
from app.categorias.service import CategoriaService

router = APIRouter(prefix="/categorias", tags=["Categorias"])
service = CategoriaService()

@router.post("/", response_model=Categoria, status_code=status.HTTP_201_CREATED)
async def create_categoria(data: CategoriaCreate, session: SessionDep):
    return service.create_categoria(data, session)

@router.get("/", response_model=list[Categoria])
async def list_categorias(session: SessionDep):
    return service.get_all(session)

@router.get("/{categoria_id}", response_model=Categoria)
async def get_categoria(categoria_id: int, session: SessionDep):
    return service.get_categoria(categoria_id, session)

@router.patch("/{categoria_id}", response_model=Categoria)
async def update_categoria(categoria_id: int, data: CategoriaUpdate, session: SessionDep):
    return service.update_categoria(categoria_id, data, session)

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(categoria_id: int, session: SessionDep):
    return service.delete_categoria(categoria_id, session)
