# piccolo_conf.py
from piccolo.engine.postgres import PostgresEngine
from piccolo.conf.apps import AppRegistry

DB = PostgresEngine(
    config={
        "database": "ea_app_db",
        "user": "postgres",
        "password": "root",
        "host": "localhost",
        "port": 5432,
    }
)



APP_REGISTRY = AppRegistry(
    apps=[
        "db.piccolo_app",
    ]
)
