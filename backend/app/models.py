from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255)
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow
    )

    cart_items: Mapped[list["CartItem"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        index=True
    )

    description: Mapped[str] = mapped_column(
        Text
    )

    # Store money as cents, not floating-point.
    price_cents: Mapped[int] = mapped_column(
        Integer
    )

    image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    category: Mapped[str] = mapped_column(
        String(100),
        index=True
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow
    )

    cart_items: Mapped[list["CartItem"]] = relationship(
        back_populates="product"
    )


class CartItem(Base):
    __tablename__ = "cart_items"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "product_id",
            name="uq_cart_user_product"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        index=True
    )

    quantity: Mapped[int] = mapped_column(
        Integer
    )

    user: Mapped[User] = relationship(
        back_populates="cart_items"
    )

    product: Mapped[Product] = relationship(
        back_populates="cart_items"
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )

    total_cents: Mapped[int] = mapped_column(
        Integer
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending",
        index=True
    )

    stripe_payment_intent_id: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        index=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow
    )

    user: Mapped[User] = relationship(
        back_populates="orders"
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        index=True
    )

    product_id: Mapped[int | None] = mapped_column(
        ForeignKey("products.id"),
        nullable=True
    )

    # Snapshot values.
    # Even if the product changes later,
    # the historical order remains correct.
    product_name: Mapped[str] = mapped_column(
        String(150)
    )

    unit_price_cents: Mapped[int] = mapped_column(
        Integer
    )

    quantity: Mapped[int] = mapped_column(
        Integer
    )

    order: Mapped[Order] = relationship(
        back_populates="items"
    )