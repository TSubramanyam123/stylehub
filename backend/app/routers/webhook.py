from fastapi import APIRouter, HTTPException, Request

from sqlalchemy import select

import stripe

from app.core.config import settings
from app.db import SessionLocal
from app.models import (
    CartItem,
    Order,
    Product
)


router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"]
)


@router.post("/stripe")
async def stripe_webhook(
    request: Request
):

    payload = await request.body()

    signature = request.headers.get(
        "stripe-signature"
    )

    if not signature:

        raise HTTPException(
            status_code=400,
            detail="Missing Stripe signature"
        )

    try:

        event = stripe.Webhook.construct_event(
            payload,
            signature,
            settings.stripe_webhook_secret
        )

    except (
        ValueError,
        stripe.error.SignatureVerificationError
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid webhook payload "
                "or signature"
            )
        )

    db = SessionLocal()

    try:

        event_type = event["type"]

        payment_intent = (
            event["data"]["object"]
        )

        payment_intent_id = (
            payment_intent.get("id")
        )

        print("Stripe event:", event_type)
        print("PaymentIntent ID:", payment_intent_id)

        if not payment_intent_id:

            return {"received": True}

        order = db.scalar(
            select(Order).where(
                Order.stripe_payment_intent_id
                == payment_intent_id
            )
        )
        print("Stripe event:", event_type)
        print("PaymentIntent ID:", payment_intent_id)
        print("Matched order:", order.id if order else "NOT FOUND")
        print(
        "Matched order:",
        order.id if order else "NOT FOUND"
        )
        
        if not order:

            return {"received": True}

        if (
            event_type
            == "payment_intent.succeeded"
        ):

            # Idempotency protection.
            if order.status != "paid":

                order.status = "paid"
                print(f"Order {order.id} status changed to paid")
                for item in order.items:

                    product = (
                        db.get(
                            Product,
                            item.product_id
                        )
                        if item.product_id
                        else None
                    )

                    if product:

                        product.stock = max(
                            0,
                            product.stock
                            - item.quantity
                        )

                db.query(
                    CartItem
                ).filter(
                    CartItem.user_id
                    == order.user_id
                ).delete(
                    synchronize_session=False
                )

        elif (
            event_type
            == "payment_intent.processing"
        ):

            order.status = "processing"

        elif (
            event_type
            == "payment_intent.payment_failed"
        ):

            order.status = "failed"

        db.commit()

        return {
            "received": True
        }

    finally:

        db.close()