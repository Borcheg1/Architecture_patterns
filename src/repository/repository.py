# thirdparty
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

# project
from src.models.domain_models import Batch
from src.repository.abstract import AbstractRepository


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, batch: Batch) -> None:
        self.session.add(batch)

    async def get(self, reference: str) -> Batch:
        result = await self.session.execute(
            select(Batch)
            .filter_by(reference=reference)
            .options(
                joinedload(Batch.product),
                selectinload(Batch.allocations),
            )
        )
        return result.scalar_one()

    async def list(self) -> list[Batch]:
        result = await self.session.execute(select(Batch))
        return result.scalars().all()
