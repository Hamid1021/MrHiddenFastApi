from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.db_config import create_db_and_tables, engine
from routers import user_router, blog_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(user_router.router)
app.include_router(blog_router.router)
