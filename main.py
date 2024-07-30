from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from domain.user import user_router
from domain.application import application_router
from domain.certificate import certificate_router

app = FastAPI()

origins = ["*"]
# "https://4x8q37-5173.csb.app/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router.router)
app.include_router(application_router.router)
app.include_router(certificate_router.router)

# @app.get("/")
# def root():
#     return {"message": "Hello World"}

# @app.put("/user")
# def user():

