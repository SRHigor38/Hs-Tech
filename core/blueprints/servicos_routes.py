"""
HS Tech — Blueprint de Serviços.

Rota da página de serviços com as 3 áreas de atuação.
"""

from flask import Blueprint, render_template

from core.utils.helpers import whatsapp_link

servicos_bp = Blueprint("servicos", __name__)


@servicos_bp.route("/servicos")
def servicos():
    """Página de serviços."""
    from core.services.content_service import get_servicos

    context = {
        "servicos": get_servicos(),
        "whatsapp_url": whatsapp_link(),
    }
    return render_template("pages/servicos.html", **context)