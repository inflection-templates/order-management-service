import datetime as dt
import uuid
from fastapi import HTTPException
from app.common.utils import print_colorized_json
from app.database.database_accessor import LocalSession
from app.database.models.users import User
from app.domain_types.schemas.users import UserCreateModel, UserResponseModel, UserUpdateModel, UserSearchFilter, UserSearchResults
from sqlalchemy.orm import Session
from app.domain_types.miscellaneous.exceptions import Conflict, NotFound
from sqlalchemy import asc, desc, func
import hashlib


def _hash_password(password: str) -> str:
    """Hash the password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return _hash_password(plain_password) == hashed_password


def get_user_by_email(session: Session, email: str) -> User:
    """Get user by email address"""
    try:
        user_obj = session.query(User).filter(User.Email == email).first()
        return user_obj
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user by email: {str(e)}")


def create_users(session: Session, model: UserCreateModel) -> UserResponseModel:
    try:
        # Check if username already exists
        existing_username = session.query(User).filter(User.UserName == model.UserName).first()
        if existing_username:
            raise HTTPException(status_code=409, detail=f"Username '{model.UserName}' already exists")
        
        # Check if email already exists
        existing_email = session.query(User).filter(User.Email == model.Email).first()
        if existing_email:
            raise HTTPException(status_code=409, detail=f"Email '{model.Email}' already exists")
        
        model_dict = model.dict()
        # Hash the password before storing
        model_dict['Password'] = _hash_password(model_dict['Password'])
        
        db_model = User(**model_dict)
        db_model.updated_at = dt.datetime.now()
        session.add(db_model)
        session.commit()
        session.refresh(db_model)
        
        print_colorized_json(db_model)
        return UserResponseModel.from_orm(db_model)
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating users: {str(e)}")


def get_users_by_id(session: Session, user_id: str) -> UserResponseModel:
    try:
        user_obj = session.query(User).filter(User.id == user_id).first()
        if not user_obj:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

        print_colorized_json(user_obj)
        return UserResponseModel.from_orm(user_obj)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user: {str(e)}")


def search_users(session: Session, filter: UserSearchFilter) -> UserSearchResults:
    try:
        query = session.query(User)

        if filter.FirstName and isinstance(filter.FirstName, str):
            query = query.filter(User.FirstName.ilike(f'%{filter.FirstName.strip()}%'))
        
        if filter.LastName and isinstance(filter.LastName, str):
            query = query.filter(User.LastName.ilike(f'%{filter.LastName.strip()}%'))
        
        if filter.UserName and isinstance(filter.UserName, str):
            query = query.filter(User.UserName.ilike(f'%{filter.UserName.strip()}%'))
        
        if filter.Email and isinstance(filter.Email, str):
            query = query.filter(User.Email.ilike(f'%{filter.Email.strip()}%'))
        
        if filter.CountryCode and isinstance(filter.CountryCode, str):
            query = query.filter(User.CountryCode == filter.CountryCode.strip())

        total_count = query.count()

        # Apply ordering
        if filter.OrderBy:
            order_column = getattr(User, filter.OrderBy, None)
            if order_column:
                if filter.OrderByDescending:
                    query = query.order_by(desc(order_column))
                else:
                    query = query.order_by(asc(order_column))

        # Apply pagination
        query = query.offset(filter.PageIndex * filter.ItemsPerPage).limit(filter.ItemsPerPage)

        items = query.all()
        response_items = [(UserResponseModel.from_orm(item) if hasattr(UserResponseModel, 'from_orm') else item.__dict__) for item in items]

        results = UserSearchResults(
            TotalCount=total_count,
            RetrievedCount=len(response_items),
            ItemsPerPage=filter.ItemsPerPage,
            PageIndex=filter.PageIndex,
            OrderBy=filter.OrderBy,
            OrderByDescending=filter.OrderByDescending,
            Items=response_items
        )

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching users: {str(e)}")


def update_users(session: Session, user_id: str, model: UserUpdateModel) -> UserResponseModel:
    try:
        user_obj = session.query(User).filter(User.id == user_id).first()
        if not user_obj:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

        update_data = model.dict(exclude_unset=True)
        
        # Check for unique constraints if updating username or email
        if 'UserName' in update_data:
            existing_username = session.query(User).filter(
                User.UserName == update_data['UserName'],
                User.id != user_id
            ).first()
            if existing_username:
                raise HTTPException(status_code=409, detail=f"Username '{update_data['UserName']}' already exists")
        
        if 'Email' in update_data:
            existing_email = session.query(User).filter(
                User.Email == update_data['Email'],
                User.id != user_id
            ).first()
            if existing_email:
                raise HTTPException(status_code=409, detail=f"Email '{update_data['Email']}' already exists")
        
        # Hash password if it's being updated
        if 'Password' in update_data:
            update_data['Password'] = _hash_password(update_data['Password'])
        
        update_data['updated_at'] = dt.datetime.now()
        
        session.query(User).filter(User.id == user_id).update(
            update_data, synchronize_session="evaluate")

        session.commit()
        session.refresh(user_obj)

        print_colorized_json(user_obj)
        return UserResponseModel.from_orm(user_obj)
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")


def delete_users(session: Session, user_id: str) -> UserResponseModel:
    try:
        user_obj = session.query(User).filter(User.id == user_id).first()
        if not user_obj:
            raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
        
        session.delete(user_obj)
        session.commit()
        
        print_colorized_json(user_obj)
        return UserResponseModel.from_orm(user_obj)
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
