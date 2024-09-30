# type: ignore
from fastapi import FastAPI
from app.routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

#----( Statement that tell sql alchemy to generate tables
# models.Base.metadata.create_all(bind=engine) ----)


# models.Base
# print("====>",dir(models.Base.metadata))

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    print("name")
    return {"message": "Welcome to FastAPI Server"}
