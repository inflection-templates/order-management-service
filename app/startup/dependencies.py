from app.database.database_connector import LocalSession, engine

def get_db_session():
    ''' Get transactional session '''
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

