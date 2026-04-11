"""
extentions.py - Este arquivo é responsável por configurar as extensões do Flask,
como o SQLAlchemy e o Migrate.
Ele define as instâncias dessas extensões que serão usadas em toda a aplicação,
e são inicializadas no arquivo __init__.py.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy()
migrate = Migrate()
