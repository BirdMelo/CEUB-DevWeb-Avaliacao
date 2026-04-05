# CONFIGURAÇÃO DA RELAÇÃO COM O BANCO DE DADOS

import os
from dotenv import load_dotenv
load_dotenv( interpolate= True )
class Config:
    _user = os.getenv("DB_USER")
    _password = os.getenv("DB_PASSWORD")
    _host = os.getenv("DB_HOST")
    _port = os.getenv("DB_PORT", "3306")
    _db = os.getenv("DB_NAME")

    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{_user}:{_password}@{_host}:{_port}/{_db}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    print("DATABASE_URL:", SQLALCHEMY_DATABASE_URI)