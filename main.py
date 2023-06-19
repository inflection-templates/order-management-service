import uvicorn
from app.common.logger import logger
from app.startup.application import app
from app.config.constants import PORT
from app.config.config import get_settings
from app.telemetry.tracing import tracing_enabled
from app.telemetry.instrumenter import instrument

# Telemetry

if tracing_enabled:
    instrument()

# Run the application server

if __name__ == "__main__":
    settings = get_settings()
    if settings.ENVIRONMENT == "development":
        logger.info("Running in development mode")
        uvicorn.run(app, host="localhost", port=PORT)
    else:
        logger.info("Running in production mode")
        uvicorn.run(app, host="0.0.0.0", port=PORT)
