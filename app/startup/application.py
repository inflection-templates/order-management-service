from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.startup.router import router
from app.common.logger import logger

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

    @server.on_event("startup")
    async def startup_event():
        """Initialize database seeding on application startup"""
        try:
            from app.startup.seeder import Seeder
            seeder = Seeder()
            seeder.init()
        except Exception as e:
            logger.error(f"Error during startup seeding: {str(e)}")
            # Don't fail startup if seeding fails, but log the error

    server.include_router(router)

    return server

app = get_application()
