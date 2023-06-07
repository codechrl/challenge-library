from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from database import db
from model.Seeds import run_seeds
from route import book, borrowing, userauth
from route.userauth import oauth2_scheme

app = FastAPI(
    title="Library API",
    version="0.1.0",
    description="API for GRIT Challenge",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
    redoc_url=None,
)

app.add_middleware(SessionMiddleware, secret_key="!secret")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healtz", status_code=status.HTTP_200_OK, tags=["Health Check"])
async def health_test():
    return {"message": "Hello!"}


app.include_router(
    userauth.router,
    prefix="/api/userauth",
    tags=["Userauth"],
    responses={
        400: {"description": "Invalid Token"},
        401: {"description": "Invalid Credential"},
        409: {"description": "Conflict"},
        201: {"description": "Created"},
    },
)

app.include_router(
    book.router,
    prefix="/api/book",
    tags=["Book"],
    dependencies=[Depends(oauth2_scheme)],
)

app.include_router(
    borrowing.router,
    prefix="/api/borrowing",
    tags=["Borrowing"],
    dependencies=[Depends(oauth2_scheme)],
)


@app.on_event("startup")
async def startup():
    await db.open_pool()
    await run_seeds()


@app.on_event("shutdown")
async def shutdown():
    await db.close_pool()


@app.get("/api/", status_code=404, include_in_schema=False)
def invalid_api():
    return {"detail": "You are got lost!"}
