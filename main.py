from fastapi import FastAPI

from domain.user import user_router
from domain.application import application_router


app = FastAPI()

app.include_router(user_router.router)
app.include_router(application_router.router)

# @app.get("/")
# def root():
#     return {"message": "Hello World"}

# @app.put("/user")
# def user():

