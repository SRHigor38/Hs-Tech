"""
HS Tech — Núcleo da aplicação.

Application Factory: cria e configura a instância do Flask.
"""

from flask import Flask, render_template

from config import Config, get_config


def create_app() -> Flask:
    """
    Cria a aplicação Flask com todas as configurações e registros.

    Returns:
        Flask: instância configurada da aplicação.
    """
    app = Flask(
        __name__,
        template_folder=str(Config.TEMPLATES_DIR),
        static_folder=str(Config.STATIC_DIR),
    )

    # Carrega configurações do ambiente ativo
    app.config.from_object(get_config())

    # Garante que os diretórios necessários existam
    Config.ensure_directories()

    # Registra os blueprints
    from core.blueprints import register_blueprints

    register_blueprints(app)

    # Registra os error handlers
    register_error_handlers(app)

    # Registra os context processors (dados globais dos templates)
    register_context_processors(app)

    # Aplica headers de segurança em todas as respostas
    apply_security_headers(app)

    # Inicializa extensões
    init_extensions(app)

    return app


def apply_security_headers(app: Flask) -> None:
    """Aplica headers de segurança em todas as respostas HTTP."""
    headers = app.config.get("SECURITY_HEADERS", {})

    @app.after_request
    def add_security_headers(response):
        for header, value in headers.items():
            response.headers[header] = value
        return response


def register_error_handlers(app: Flask) -> None:
    """Registra os handlers de erro personalizados."""

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500


def register_context_processors(app: Flask) -> None:
    """Injeta dados globais disponíveis em todos os templates."""
    from core.utils.helpers import current_year, empresa_config, whatsapp_link

    @app.context_processor
    def inject_globals():
        return {
            "ano_atual": current_year(),
            "empresa": empresa_config(),
            "whatsapp_url": whatsapp_link(),
        }


def init_extensions(app: Flask) -> None:
    """
    Inicializa as extensões do Flask.

    Futuro: SQLAlchemy, Migrate, LoginManager serão ativados aqui.
    """
    from core.extensions import load_extensions

    load_extensions(app)