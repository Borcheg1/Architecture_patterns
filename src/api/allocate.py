# thirdparty
from sqlalchemy.ext.asyncio.session import AsyncSession

# fastapi
from fastapi import APIRouter, Depends, status

# project
from src.db.db import get_session
from src.models.domain_models import OrderLine, allocate
from src.repository.repository import SqlAlchemyRepository

router = APIRouter(prefix="/allocate")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=list[str])
async def allocate_endpoint(order_lines: list[OrderLine], session: AsyncSession = Depends(get_session)) -> list[str]:
    batches = await SqlAlchemyRepository(session=session).list()
    batch_refs = [allocate(line, batches) for line in order_lines]
    await session.commit()
    return batch_refs
