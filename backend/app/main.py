from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db import Base, engine

from app.routers import (
    auth,
    products,
    cart,
    orders,
    webhook
)


@asynccontextmanager
async def lifespan(
    _: FastAPI
):

    Base.metadata.create_all(
        bind=engine
    )

    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=(
        settings.cors_origin_list
    ),

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


app.include_router(
    auth.router,
    prefix="/api/v1"
)

app.include_router(
    products.router,
    prefix="/api/v1"
)

app.include_router(
    cart.router,
    prefix="/api/v1"
)

app.include_router(
    orders.router,
    prefix="/api/v1"
)

app.include_router(
    webhook.router,
    prefix="/api/v1"
)


@app.get("/health")
def health():

    return {
        "status": "ok"
    }