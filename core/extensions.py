"""Extensões compartilhadas (db, login, csrf, limiter).

Centralizar aqui evita importações circulares entre models e routes.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import current_app, request
from ipaddress import ip_address

def client_limit_key():
    """Use CF-Connecting-IP somente no web service público atrás da borda Render."""
    if current_app.config.get('TRUST_RENDER_CF_IP'):
        try:
            return str(ip_address(request.headers.get('CF-Connecting-IP', '')))
        except ValueError:
            # Não confie em X-Forwarded-For; ausência de cabeçalho compartilha limite.
            return 'render-header-ausente'
    return get_remote_address()


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=client_limit_key,
)

login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para continuar."
login_manager.login_message_category = "warning"


def load_extensions(app) -> None:
    """Inicializa todas as extensões da aplicação.

    Atualmente ativa:
    - SQLAlchemy (banco de dados)
    - Flask-Login (autenticação de sessão)
    - CSRF protection

    Futuro: Flask-Migrate, Flask-Limiter com armazenamento persistente.
    """
    # SQLAlchemy
    db.init_app(app)
    migrate.init_app(app, db)

    # Flask-Login
    login_manager.init_app(app)

    # CSRF Protection
    csrf.init_app(app)

    # Flask-Limiter (storage em memória para demonstração)
    limiter.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from core.models import Administrador
    try:
        return db.session.get(Administrador, int(user_id))
    except (ValueError, TypeError):
        return None
