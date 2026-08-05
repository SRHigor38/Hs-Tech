"""
HS Tech — Blueprint de Projetos.

Rota da página de portfólio (projetos).
"""

from flask import Blueprint, render_template

from core.utils.helpers import whatsapp_link

projetos_bp = Blueprint("projetos", __name__)


@projetos_bp.route("/projetos")
def projetos():
    """Página de projetos (portfólio)."""
    from core.services.content_service import get_projetos

    context = {
        "projetos": get_projetos(),
        "categorias": ["Todos", "Sites", "Sistemas", "Automações", "Computadores"],
        "whatsapp_url": whatsapp_link(),
    }
    return render_template("pages/projetos.html", **context)