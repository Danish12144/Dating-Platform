# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routes import (
    auth,
    users,
    discovery,
    swipe,
    chat,
    admin,
    media,
)

def get_application() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---- Register routers -------------------------------------------------
    app.include_router(auth.router, prefix=settings.API_V1_STR)
    app.include_router(users.router, prefix=settings.API_V1_STR)
    app.include_router(discovery.router, prefix=settings.API_V1_STR)
    app.include_router(swipe.router, prefix=settings.API_V1_STR)
    app.include_router(chat.router, prefix=settings.API_V1_STR)
    app.include_router(admin.router, prefix=settings.API_V1_STR)
    app.include_router(media.router, prefix=settings.API_V1_STR)

    return app


app = get_application()
