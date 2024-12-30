from fastapi import FastAPI
from routers import user_router, blog_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     create_db_and_tables()
#     yield
#     await engine.dispose()

# app = FastAPI(lifespan=lifespan)
app = FastAPI()

app.include_router(user_router.router)
app.include_router(blog_router.router)
