import fastapi
from starlette.middleware.cors import CORSMiddleware

from app.api import line_user_router
from config.settings.base import settings


def initialize_backend_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI()

    # CORSの設定
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )

    # ルーティングの設定
    app.include_router(router=line_user_router.router)

    return app
