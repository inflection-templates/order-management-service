from fastapi import APIRouter, Depends, status
from app.api.cart.cart_handler import (
    create_cart_,
    get_cart_by_id_,
    update_cart_,
    delete_cart_,
    search_carts_
)
from app.database.database_accessor import get_db_session
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.cart import CartCreateModel, CartResponseModel, CartUpdateModel, CartSearchFilter, CartSearchResults

###############################################################################

router = APIRouter(
    prefix="/carts",
    tags=["carts"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseModel[CartResponseModel|None])
async def create_cart(model: CartCreateModel, db_session = Depends(get_db_session)):
    return create_cart_(model, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[CartSearchResults|None])
async def search_cart(
        query_params: CartSearchFilter = Depends(),
        db_session = Depends(get_db_session)):
    filter = CartSearchFilter(**query_params.dict())
    return search_carts_(filter, db_session)

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[CartResponseModel|None])
async def get_cart_by_id(id: str, db_session = Depends(get_db_session)):
    return get_cart_by_id_(id, db_session)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[CartResponseModel|None])
async def update_cart(id: str, model: CartUpdateModel, db_session = Depends(get_db_session)):
    return update_cart_(id, model, db_session)

@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=ResponseModel[bool])
async def delete_cart(id: str, db_session = Depends(get_db_session)):
    return delete_cart_(id, db_session)

@router.get("/search", status_code=status.HTTP_200_OK, response_model=ResponseModel[CartSearchResults|None])
async def search_cart(
        query_params: CartSearchFilter = Depends(),
        db_session = Depends(get_db_session)):
    filter = CartSearchFilter(**query_params.dict())
    return search_carts_(filter, db_session)
