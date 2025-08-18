from app.common.utils import validate_uuid4
from app.database.services import users_service
from app.domain_types.miscellaneous.response_model import ResponseModel
from app.domain_types.schemas.users import UserResponseModel, UserSearchResults, DeleteResponseModel


def create_users_(model, db_session):
    try:
        users = users_service.create_users(db_session, model)
        message = "User created successfully"
        resp = ResponseModel[UserResponseModel](
            Message=message, Data=users, HttpCode=201)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()


def get_users_by_id_(id, db_session):
    try:
        users_id = validate_uuid4(id)
        users = users_service.get_users_by_id(db_session, users_id)
        message = "User retrieved successfully"
        resp = ResponseModel[UserResponseModel](
            Message=message, Data=users, HttpCode=200)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()


def search_users_(filter, db_session):
    try:
        users = users_service.search_users(db_session, filter)
        message = "Users retrieved successfully"
        resp = ResponseModel[UserSearchResults](Message=message, Data=users, HttpCode=200)
        return resp
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.close()


def update_users_(id, model, db_session):
    try:
        users_id = validate_uuid4(id)
        users = users_service.update_users(db_session, users_id, model)
        message = "User updated successfully"
        resp = ResponseModel[UserResponseModel](Message=message, Data=users, HttpCode=200)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()


def delete_users_(id, db_session):
    try:
        users_id = validate_uuid4(id)
        users = users_service.delete_users(db_session, users_id)
        message = "User deleted successfully"
        delete_response = DeleteResponseModel(deleted=True)
        resp = ResponseModel[DeleteResponseModel](
            Message=message, Data=users, HttpCode=200)
        # logger.info(resp)
        return resp
    except Exception as e:
        print(e)
        db_session.rollback()
        raise e
    finally:
        db_session.close()


