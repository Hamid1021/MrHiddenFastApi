from fastapi import FastAPI
from routers import user_router, blog_router, authenticate

app = FastAPI()

app.include_router(user_router.router, tags=["Users"])
app.include_router(blog_router.router, tags=["Blogs"])
app.include_router(authenticate.router, tags=["Authenticate"])

# Start the server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=3000)
