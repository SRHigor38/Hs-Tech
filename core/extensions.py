"""
HS Tech — Extensões do Flask.

Centraliza as instâncias das extensões para evitar imports circulares.

Futuro (quando o banco for ativado):
    - from flask_sqlalchemy import SQLAlchemy
    - from flask_migrate import Migrate
    - from flask_login import LoginManager

    db = SQLAlchemy()
    migrate = Migrate()
    login_manager = LoginManager()
"""


def load_extensions(app) -> None:
    """
    Inicializa todas as extensões da aplicação.

    Atualmente não há extensões ativas.
    Futuramente, basta descomentar os imports e chamar:

        db.init_app(app)
        migrate.init_app(app, db)
        login_manager.init_app(app)
    """
    # Ativação futura:
    # from core.extensions import db
    # db.init_app(app)

    return None