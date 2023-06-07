from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from startup.router import router
from app.config.constants import API_PREFIX, API_VERSION

app = FastAPI()

def add_middlewares(app: FastAPI):

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    # Add middleware to handle exceptions


add_middlewares(app)
app.include_router(router)
