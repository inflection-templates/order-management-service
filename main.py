import uvicorn
from app.startup.application import get_application
from app.config.constants import PORT
from app.config import settings

app = get_application()

if __name__ == "__main__":
    if settings.ENVIRONMENT == "development":
        uvicorn.run(app, host="localhost", port=PORT)
    else:
        uvicorn.run(app, host="0.0.0.0", port=PORT)
