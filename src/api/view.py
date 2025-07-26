from tronpy import AsyncTron, Tron
from fastapi import Depends, HTTPException
from tronpy.providers import AsyncHTTPProvider, HTTPProvider
from pydantic import BaseModel
from sqlalchemy import select
from src.database.database import get_session
from src.database.models import AddrRequest, Query, PaginationDep

async def get_info(addr: str, db = Depends(get_session)):
    async with AsyncTron(AsyncHTTPProvider(api_key='2955947c-1c12-4b4e-9f9e-a31ae1b12192'), network='mainnet') as client:
        
        account = await client.get_account(addr)
        bandwidth = await client.get_bandwidth(addr)

        try:
            energy = account['account_resource']['energy_window_size']
            name = account['account_name']
        except:
            energy = 0
            name = 'blankname'

        db_request = Query(
            name = name,
            adress = addr,
            bandwidth = bandwidth,
            energy = energy,
            trx = account['balance']
        )

        db.add(db_request)
        await db.commit()
        await db.refresh(db_request)

        return db_request
    
async def get_info_db(pagin: PaginationDep, db = Depends(get_session)):
    statement = select(Query).order_by(Query.id.desc()).offset(pagin.offset).limit(pagin.limit)
    result = await db.execute(statement)
    return result.scalars().all()
