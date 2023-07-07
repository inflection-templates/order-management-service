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
    alembic init alembic
    ```
    It will generate a migration directory `alembic` and `alembic.ini` file in project root directory.
4. Edit `alembic.ini` file for databse URL. Replace the database URL at `sqlalchemy.url` field in `alembic.ini` file with your database URL. In this case:
    `sqlalchemy.url = mysql+pymysql://dbuser:dbpassword@localhost:3306/order_management`

5. Go to newly created `alembic` directory. Modify `env.py` file as:
    1. Import all database models from `models` dirctory.
    2. Import `Base`.
    3. Edit `target_metadata` as `target_metadata = Base.metadata`

6. Create a new revision using command:
    ```
    alembic revision --autogenerate
    ```
7. If you get error like `ERROR [alembic.util.messaging] Target database is not up to date.`, run following command and then again try to create revision:
    ```
    alembic upgrade head
    ```
    This command will apply any pending migrations to bring the target database up to date.

