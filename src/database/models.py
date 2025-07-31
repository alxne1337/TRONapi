from fastapi import Depends
from sqlmodel import SQLModel, Field
from typing import Annotated, Optional
from pydantic import BaseModel
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Query(SQLModel, table=True):
    __tablename__ = 'query'
    id: Annotated[Optional[int], Field(primary_key=True, default=None)]
    name: Annotated[str, Field(default=None)]
    adress: str
    bandwidth: Annotated[int, Field(default=None)]
    energy: Annotated[int, Field(default=None)]
    trx: Annotated[int, Field(default=None)]

class AddrRequest(BaseModel):
    addr: str

class Pagination(BaseModel):
    limit: Annotated[int, Field(5, ge=1, le=20, description='Кол-во элементов в одной странице запроса')]
    offset: Annotated[int, Field(0, ge=0, description='Номер страницы')]


PaginationDep=Annotated[Pagination, Depends(Pagination)]