from fastapi import FastAPI

from app.utils.logging import get_custom_logger


log = get_custom_logger("grantbot")


app = FastAPI()

#app.include_router()