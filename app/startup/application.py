from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.startup.router import router

#################################################################

def get_application():

    server = FastAPI()

    # Add CORS middleware
    server.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    server.include_router(router)

    return server

app = get_application()
