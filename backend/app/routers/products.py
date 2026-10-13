from fastapi import APIRouter, HTTPException

from sqlalchemy import select

from app.dependencies import DBSession
from app.models import Product
from app.schemas import ProductOut


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get(
    "",
    response_model=list[ProductOut]
)
def list_products(
    db: DBSession
):

    return list(
        db.scalars(
            select(Product)
            .where(Product.is_active.is_(True))
            .order_by(Product.id.desc())
        ).all()
    )


@router.get(
    "/{product_id}",
    response_model=ProductOut
)
def get_product(
    product_id: int,
    db: DBSession
):

    product = db.get(
        Product,
        product_id
    )

    if not product or not product.is_active:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product