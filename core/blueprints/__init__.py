"""
HS Tech — Registro central de Blueprints.

Todos os blueprints da aplicação são registrados aqui.
Novos módulos (admin, api, blog) bastam ser adicionados nesta função.
"""

from flask import Flask


def register_blueprints(app: Flask) -> None:
    """Registra todos os blueprints da aplicação."""
    from core.blueprints.main_routes import main_bp
    from core.blueprints.servicos_routes import servicos_bp
    from core.blueprints.projetos_routes import projetos_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(servicos_bp)
    app.register_blueprint(projetos_bp)