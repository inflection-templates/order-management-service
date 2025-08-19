import datetime as dt
from app.common.utils import print_colorized_json
from app.database_sqlmodel.models.cart import Cart
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from app.domain_types.schemas.cart import CartCreateModel, CartResponseModel, CartUpdateModel, CartSearchFilter, CartSearchResults
from sqlmodel import UUID, Session, asc, desc, select
from app.telemetry.tracing import trace_span

@trace_span("service: create_cart")
def create_cart(session: Session, model: CartCreateModel) -> CartResponseModel:
    model_dict = model.dict()
    db_model = Cart(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    session.refresh(db_model)
    cart = db_model
    return cart.dict()

@trace_span("service: get_cart_by_id")
def get_cart_by_id(session: Session, cart_id: str) -> CartResponseModel:
    cart = session.exec(select(Cart).where(Cart.id == cart_id)).first()
    if not cart:
        raise NotFound(f"Cart with id {cart_id} not found")
    return cart.dict()

@trace_span("service: update_cart")
def update_cart(session: Session, cart_id: str, model: CartUpdateModel) -> CartResponseModel:
    cart = session.exec(select(Cart).where(Cart.id == cart_id)).first()
    if not cart:
        raise NotFound(f"Cart with id {cart_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.execute(select(Cart).where(Cart.id == cart_id).update(update_data, synchronize_session="auto"))

    session.commit()
    session.refresh(cart)
    return cart.dict()

@trace_span("service: delete_cart")
def delete_cart(session: Session, cart_id: str):
    cart = session.exec(select(Cart).where(Cart.id == cart_id)).first()
    if not cart:
        raise NotFound(f"Cart with id {cart_id} not found")
    session.delete(cart)
    session.commit()
    return True

@trace_span("service: search_carts")
def search_carts(session: Session, filter: CartSearchFilter) -> CartSearchResults:

    query = select(Cart)

    if filter.CustomerId:
        query = query.where(Cart.CustomerId.like(f'%{filter.CustomerId}%'))
    if filter.ProductId:
        query = query.where(Cart.ProductId == filter.ProductId)
    if filter.TotalItemsCountGreaterThan:
        query = query.where(Cart.TotalItemsCount > filter.TotalItemsCountGreaterThan)
    if filter.TotalItemsCountLessThan:
        query = query.where(Cart.TotalItemsCount < filter.TotalItemsCountLessThan)
    if filter.TotalAmountGreaterThan:
        query = query.where(Cart.TotalAmount > filter.TotalAmountGreaterThan)
    if filter.TotalAmountLessThan:
        query = query.where(Cart.TotalAmount < filter.TotalAmountLessThan)
    if filter.CreatedBefore:
        query = query.where(Cart.CreatedAt < filter.CreatedBefore)
    if filter.CreatedAfter:
        query = query.where(Cart.CreatedAt > filter.CreatedAfter)

    if filter.OrderBy is None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(Cart, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    orderBy = getattr(Cart, filter.OrderBy)

    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))

    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

    carts = session.exec(query).all()

    items = list(map(lambda x: x.dict(), carts))

    results = CartSearchResults(
        TotalCount=len(carts),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )

    return results
