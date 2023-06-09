from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.startup.router import router

def get_application():

    app = FastAPI()

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(router)

    return app
