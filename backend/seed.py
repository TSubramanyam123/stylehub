from app.db import (
    Base,
    SessionLocal,
    engine
)

from app.models import Product


products = [

    {
        "name": "Classic Denim Jacket",
        "description": "Mid-weight denim jacket with a clean everyday fit.",
        "price_cents": 4999,
        "category": "Jackets",
        "stock": 20,
        "image_url": "https://images.unsplash.com/photo-1551028719-00167b16eac5?auto=format&fit=crop&w=800&q=80"
    },

    {
        "name": "Minimal White Tee",
        "description": "Soft cotton crew-neck t-shirt for everyday styling.",
        "price_cents": 1999,
        "category": "T-Shirts",
        "stock": 50,
        "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=800&q=80"
    },

    {
        "name": "Relaxed Cargo Pants",
        "description": "Relaxed-fit cargo pants with utility pockets.",
        "price_cents": 3599,
        "category": "Pants",
        "stock": 30,
        "image_url": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=800&q=80"
    },

    {
        "name": "Everyday Sneakers",
        "description": "Low-profile sneakers designed for daily wear.",
        "price_cents": 5499,
        "category": "Footwear",
        "stock": 25,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80"
    }

]


Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:

    if db.query(Product).count() == 0:

        db.add_all(
            [
                Product(**product)
                for product in products
            ]
        )

        db.commit()

        print("Products seeded.")

    else:

        print("Products already exist.")

finally:

    db.close()