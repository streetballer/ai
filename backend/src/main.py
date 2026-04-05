from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.common.libraries.database import close_database
from src.common.middleware.error_handler import register_error_handlers
from src.common.routes.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    close_database()


app = FastAPI(lifespan=lifespan)

register_error_handlers(app)

app.include_router(router)
