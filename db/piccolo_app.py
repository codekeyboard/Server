from piccolo.conf.apps import AppConfig
from models.AppUser import AppUser  

APP_CONFIG = AppConfig(
    app_name="db",
    migrations_folder_path="/home/x/Documents/repo/EigenAgents/project/servers/app/db/migrations",
    table_classes=[AppUser],
)
