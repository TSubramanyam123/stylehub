from fastapi import APIRouter, HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import selectinload

import stripe

from app.core.config import settings
from app.dependencies import CurrentUser, DBSession
from app.models import (
    CartItem,
    Order,
    OrderItem
)
from app.schemas import (
    OrderOut,
    OrderItemOut,
    PaymentIntentOut
)


stripe.api_key = settings.stripe_secret_key


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


def order_to_schema(
    order: Order
) -> OrderOut:

    return OrderOut(
        id=order.id,
        total_cents=order.total_cents,
        status=order.status,
        stripe_payment_intent_id=(
            order.stripe_payment_intent_id
        ),
        created_at=order.created_at,

        items=[
            OrderItemOut(
                product_id=item.product_id,
                product_name=item.product_name,
                unit_price_cents=item.unit_price_cents,
                quantity=item.quantity,
                line_total_cents=(
                    item.quantity
                    * item.unit_price_cents
                )
            )

            for item in order.items
        ]
    )


@router.post(
    "/create-payment-intent",
    response_model=PaymentIntentOut,
    status_code=status.HTTP_201_CREATED
)
def create_order_and_payment(
    current_user: CurrentUser,
    db: DBSession
):

    cart_items = list(
        db.scalars(
            select(CartItem)
            .options(
                selectinload(CartItem.product)
            )
            .where(
                CartItem.user_id
                == current_user.id
            )
        ).all()
    )

    if not cart_items:

        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    total = 0

    for item in cart_items:

        product = item.product

        if not product.is_active:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Product '{product.name}' "
                    "is unavailable"
                )
            )

        if item.quantity > product.stock:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Only {product.stock} "
                    f"of '{product.name}' available"
                )
            )

        total += (
            item.quantity
            * product.price_cents
        )

    # Create local order first.
    order = Order(
        user_id=current_user.id,
        total_cents=total,
        status="pending"
    )

    db.add(order)

    db.flush()

    # Snapshot product information.
    for item in cart_items:

        order.items.append(
            OrderItem(
                product_id=item.product_id,
                product_name=item.product.name,
                unit_price_cents=(
                    item.product.price_cents
                ),
                quantity=item.quantity
            )
        )

    db.commit()
    db.refresh(order)

    try:

        payment_intent = (
            stripe.PaymentIntent.create(

                amount=total,

                currency="usd",

                automatic_payment_methods={
                    "enabled": True
                },

                metadata={
                    "order_id": str(order.id),
                    "user_id": str(current_user.id)
                },

                description=(
                    f"StyleHub order #{order.id}"
                ),

                receipt_email=current_user.email
            )
        )

    except stripe.StripeError as exc:

        order.status = "failed"

        db.commit()

        raise HTTPException(
            status_code=502,
            detail=(
                "Payment provider error: "
                f"{exc.user_message or str(exc)}"
            )
        )

    order.stripe_payment_intent_id = (
        payment_intent.id
    )

    db.commit()
    db.refresh(order)

    return PaymentIntentOut(
        order=order_to_schema(order),
        client_secret=payment_intent.client_secret,
        publishable_key=(
            settings.stripe_publishable_key
        )
    )


@router.get(
    "",
    response_model=list[OrderOut]
)
def list_orders(
    current_user: CurrentUser,
    db: DBSession
):

    orders = db.scalars(
        select(Order)
        .options(
            selectinload(Order.items)
        )
        .where(
            Order.user_id
            == current_user.id
        )
        .order_by(
            Order.created_at.desc()
        )
    ).all()

    return [
        order_to_schema(order)
        for order in orders
    ]


@router.get(
    "/{order_id}",
    response_model=OrderOut
)
def get_order(
    order_id: int,
    current_user: CurrentUser,
    db: DBSession
):

    order = db.scalar(
        select(Order)
        .options(
            selectinload(Order.items)
        )
        .where(
            Order.id == order_id,
            Order.user_id == current_user.id
        )
    )

    if not order:

        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order_to_schema(order)