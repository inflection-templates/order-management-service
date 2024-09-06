import datetime as dt
import json
from fastapi import Query, Body
from app.common.utils import print_colorized_json
from app.database.database_accessor import LocalSession
from app.database.models.role import Role
from app.domain_types.schemas.role.role import RoleCreateModel, RoleResponseModel, RoleSearchFilter, RoleSearchResults, RoleUpdateModel
from sqlalchemy.orm import Session
from app.domain_types.miscellaneous.exceptions import NotFound
from sqlalchemy import asc, desc, func
from app.telemetry.tracing import trace_span

###############################################################################

@trace_span("service: create_role")
def create_role(session: Session, model: RoleCreateModel) -> RoleResponseModel:
    model_dict = model.dict()
    db_model = Role(**model_dict)
    db_model.UpdatedAt = dt.datetime.now()
    session.add(db_model)
    session.commit()
    temp = session.refresh(db_model)
    role = db_model

    print_colorized_json(role)
    return role.__dict__

@trace_span("service: get_role_by_id")
def get_role_by_id(session: Session, role_id: str) -> RoleResponseModel:
    role = session.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise NotFound(f"Role with id {role_id} not found")

    print_colorized_json(role)
    return role.__dict__

@trace_span("service: update_role")
def update_role(session: Session, role_id: int, model: RoleUpdateModel) -> RoleResponseModel:
    role = session.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise NotFound(f"Role with id {role_id} not found")

    update_data = model.dict(exclude_unset=True)
    update_data["UpdatedAt"] = dt.datetime.now()
    session.query(Role).filter(Role.id == role_id).update(
        update_data, synchronize_session="auto")

    session.commit()
    session.refresh(role)

    print_colorized_json(role)
    return role.__dict__

@trace_span("service: search_roles")
def search_roles(session: Session, filter: RoleSearchFilter) -> RoleSearchResults:

    query = session.query(Role)

    if filter.RoleName:
        query = query.filter(Role.RoleName.like(f'%{filter.RoleName}%'))
    if filter.OrderBy == None:
        filter.OrderBy = "CreatedAt"
    else:
        if not hasattr(Role, filter.OrderBy):
            filter.OrderBy = "CreatedAt"
    orderBy = getattr(Role, filter.OrderBy)

    if filter.OrderByDescending:
        query = query.order_by(desc(orderBy))
    else:
        query = query.order_by(asc(orderBy))

    query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

    roles = query.all()

    items = list(map(lambda x: x.__dict__, roles))

    results = RoleSearchResults(
        TotalCount=len(roles),
        ItemsPerPage=filter.ItemsPerPage,
        PageIndex=filter.PageIndex,
        OrderBy=filter.OrderBy,
        OrderByDescending=filter.OrderByDescending,
        Items=items
    )

    return results

@trace_span("service: delete_role")
def delete_role(session: Session, role_id: str) -> RoleResponseModel:
    role = session.query(Role).get(role_id)
    if not role:
        raise NotFound(f"Role with id {role_id} not found")

    session.delete(role)

    session.commit()

    print_colorized_json(role)
    return role.__dict__