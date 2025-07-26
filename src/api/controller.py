from fastapi import APIRouter, Depends
from src.database.database import get_session
from src.database.models import Query, AddrRequest, PaginationDep
from src.api.view import get_info, get_info_db
from typing import Annotated, List

router = APIRouter(prefix='/API', tags = ['API'])

@router.post('/fromAPI', response_model=Query)
async def get_info_from_api(addr: str, db = Depends(get_session)):
    response = await get_info(addr, db)
    return response

@router.post('/fromDB', response_model=List[Query])
async def get_from_db(pagin: PaginationDep, db = Depends(get_session)):
    response = await get_info_db(pagin, db)
    return response