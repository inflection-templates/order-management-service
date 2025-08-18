from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.domain_types.schemas.auth import LoginModel, LoginResponseModel, TokenData
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.common.auth_decorators import authenticate_required
from app.database.database_accessor import get_db_session
from app.api.auth.auth_handler import login_, get_current_user_info_, logout_

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=ResponseModel[LoginResponseModel | None])
async def login(login_data: LoginModel, db_session: Session = Depends(get_db_session)):
    """Authenticate user and return JWT token"""
    return login_(login_data, db_session)


@router.get("/me", response_model=ResponseModel[TokenData | None])
@authenticate_required
async def get_current_user_info(
    request: Request,
    current_user: TokenData = None  # Injected by decorator
):
    """Get current user information - requires authentication"""
    return get_current_user_info_(current_user)


@router.post("/logout")
@authenticate_required
async def logout(
    request: Request,
    current_user: TokenData = None
):
    """Logout user - requires authentication"""
    return logout_()
