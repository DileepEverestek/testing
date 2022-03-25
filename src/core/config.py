import os
from dotenv import load_dotenv

from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME:str = "testfast"
    PROJECT_VERSION: str = "1.0.0"

    MYSQL_USER : str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_SERVER : str = os.getenv("MYSQL_SERVER","localhost")
    MYSQL_PORT : str = os.getenv("MYSQL_PORT",5432) # default postgres port is 5432
    MYSQL_DB : str = os.getenv("MYSQL_DB","tdd")
    DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"

settings = Settings()




