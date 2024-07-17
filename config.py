import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()

class Settings():
  MYSQL_HOST = os.environ.get("MYSQL_HOST")
  MYSQL_PORT = int(os.environ.get("MYSQL_PORT"))
  MYSQL_USER = os.environ.get("MYSQL_USER")
  MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
  MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
  SECRET_KEY = os.environ.get("SECRET_KEY")
  ALGORITHM = os.environ.get("ALGORITHM")
  

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()