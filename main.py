from fastapi import FastAPI
from routers import user_router, blog_router, authenticate
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router, tags=["Users"])
app.include_router(blog_router.router, tags=["Blogs"])
app.include_router(authenticate.router, tags=["Authenticate"])

# Start the server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=3000)
