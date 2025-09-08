# fastapi
from fastapi import APIRouter, Request

# project
from db.db import get_session
from models.domain_models import Batch, OrderLine, Product, allocate

router = APIRouter(prefix="/allocate")


@router.post("/")
async def allocate_endpoint(request: Request):
    session = get_session()

    # extract order line from request
    line = OrderLine(
        request["order_id"],
        Product(request["title"]),
        request["quantity"],
    )

    # load all batches from the DB
    batches = session.query(Batch).all()

    # call our domain service
    allocate(line, batches)

    # save the allocation back to the database
    session.commit()

    return 201
