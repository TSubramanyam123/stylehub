from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field
)


# ==========================================
# AUTHENTICATION
# ==========================================

class UserCreate(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=72
    )


class UserOut(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    email: EmailStr
    is_active: bool
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ==========================================
# PRODUCTS
# ==========================================

class ProductCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=150
    )

    description: str

    price_cents: int = Field(
        gt=0
    )

    image_url: str | None = None

    category: str

    stock: int = Field(
        ge=0
    )


class ProductOut(ProductCreate):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    is_active: bool


# ==========================================
# CART
# ==========================================

class CartItemCreate(BaseModel):
    product_id: int

    quantity: int = Field(
        default=1,
        ge=1,
        le=50
    )


class CartItemUpdate(BaseModel):
    quantity: int = Field(
        ge=1,
        le=50
    )


class CartItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductOut
    line_total_cents: int


class CartOut(BaseModel):
    items: list[CartItemOut]
    total_cents: int


# ==========================================
# ORDERS
# ==========================================

class OrderItemOut(BaseModel):
    product_id: int | None
    product_name: str
    unit_price_cents: int
    quantity: int
    line_total_cents: int


class OrderOut(BaseModel):
    id: int
    total_cents: int
    status: str
    stripe_payment_intent_id: str | None
    created_at: datetime
    items: list[OrderItemOut]


# ==========================================
# STRIPE PAYMENT
# ==========================================

class PaymentIntentOut(BaseModel):
    order: OrderOut
    client_secret: str
    publishable_key: str