## Alembic Migration

1. Activate virtual environment.(Windows OS)
    ```
    .\env\Scripts\activate
    ```
2. Install `alembic`.
    ```
    pip install alembic
    ```
3. Create a migration environment.
    ```
    alembic init alembic_sqlmodel
    ```
    It will generate a migration directory `alembic_sqlmodel` and `alembic_sqlmodel.ini` file in project root directory.
4. Edit `alembic_sqlmodel.ini` file for databse URL. Replace the database URL at `sqlalchemy.url` field in `alembic_sqlmodel.ini` file with your database URL. In this case:
    `sqlalchemy.url = mysql+pymysql://dbuser:dbpassword@localhost:3306/order_management`

5. Go to newly created `alembic_sqlmodel` directory. Modify `env.py` file as:
    1. Import all database models from `models` dirctory.
    2. Import `Base`.
    3. Edit `target_metadata` as `target_metadata = Base.metadata`

6. Create a new revision using command:
    ```
    alembic revision --autogenerate
    OR
    alembic -c alembic_sqlmodel.ini revision --autogenerate -m "Initial migration"
    ```
7. If you get error like `ERROR [alembic.util.messaging] Target database is not up to date.`, run following command and then again try to create revision:
    ```
    alembic upgrade head
    OR
    alembic -c alembic_sqlmodel.ini upgrade head
    ```
    This command will apply any pending migrations to bring the target database up to date.