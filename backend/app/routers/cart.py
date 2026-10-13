from fastapi import APIRouter, HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.dependencies import CurrentUser, DBSession
from app.models import CartItem, Product
from app.schemas import (
    CartItemCreate,
    CartItemOut,
    CartItemUpdate,
    CartOut
)


router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


def build_cart(
    db,
    user_id: int
) -> CartOut:

    items = list(
        db.scalars(
            select(CartItem)
            .options(
                joinedload(CartItem.product)
            )
            .where(
                CartItem.user_id == user_id
            )
            .order_by(CartItem.id)
        ).all()
    )

    output = []

    for item in items:

        line_total = (
            item.quantity
            * item.product.price_cents
        )

        output.append(
            CartItemOut(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                product=item.product,
                line_total_cents=line_total
            )
        )

    total = sum(
        item.line_total_cents
        for item in output
    )

    return CartOut(
        items=output,
        total_cents=total
    )


@router.get(
    "",
    response_model=CartOut
)
def get_cart(
    current_user: CurrentUser,
    db: DBSession
):

    return build_cart(
        db,
        current_user.id
    )


@router.post(
    "/items",
    response_model=CartOut,
    status_code=status.HTTP_201_CREATED
)
def add_to_cart(
    payload: CartItemCreate,
    current_user: CurrentUser,
    db: DBSession
):

    product = db.get(
        Product,
        payload.product_id
    )

    if not product or not product.is_active:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    existing = db.scalar(
        select(CartItem)
        .where(
            CartItem.user_id == current_user.id,
            CartItem.product_id == product.id
        )
    )

    current_quantity = (
        existing.quantity
        if existing
        else 0
    )

    new_quantity = (
        current_quantity
        + payload.quantity
    )

    if new_quantity > product.stock:

        raise HTTPException(
            status_code=400,
            detail=f"Only {product.stock} item(s) available"
        )

    if existing:

        existing.quantity = new_quantity

    else:

        db.add(
            CartItem(
                user_id=current_user.id,
                product_id=product.id,
                quantity=payload.quantity
            )
        )

    db.commit()

    return build_cart(
        db,
        current_user.id
    )


@router.patch(
    "/items/{item_id}",
    response_model=CartOut
)
def update_cart(
    item_id: int,
    payload: CartItemUpdate,
    current_user: CurrentUser,
    db: DBSession
):

    item = db.scalar(
        select(CartItem)
        .options(
            joinedload(CartItem.product)
        )
        .where(
            CartItem.id == item_id,
            CartItem.user_id == current_user.id
        )
    )

    if not item:

        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    if payload.quantity > item.product.stock:

        raise HTTPException(
            status_code=400,
            detail=f"Only {item.product.stock} item(s) available"
        )

    item.quantity = payload.quantity

    db.commit()

    return build_cart(
        db,
        current_user.id
    )


@router.delete(
    "/items/{item_id}",
    response_model=CartOut
)
def remove_from_cart(
    item_id: int,
    current_user: CurrentUser,
    db: DBSession
):

    item = db.scalar(
        select(CartItem)
        .where(
            CartItem.id == item_id,
            CartItem.user_id == current_user.id
        )
    )

    if not item:

        raise HTTPException(
            status_code=404,
            detail="Cart item not found"
        )

    db.delete(item)
    db.commit()

    return build_cart(
        db,
        current_user.id
    )