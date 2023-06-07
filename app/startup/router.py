from fastapi import APIRouter, Depends, HTTPException, status
from app.config.constants import API_PREFIX, API_VERSION
from app.api.api_router import router as api_router
from app.config.constants import PORT, SERVICE_NAME

router = APIRouter()

@router.get('/', status_code=200)
def service():
    return "{service} is running on port {port}".format(service=SERVICE_NAME, port=PORT)

@router.get('/health-check', status_code=200)
def perform_healthcheck():
    return "OK"

# Add API outer here...
router.include_router(api_router)
