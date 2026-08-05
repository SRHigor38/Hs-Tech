"""
HS Tech — Blueprint principal.

Rotas institucionais: Home, Sobre e Contato.
"""

from flask import Blueprint, render_template

from core.utils.helpers import whatsapp_link

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """Página inicial."""
    from core.services.content_service import (
        get_servicos_destaque,
        get_projetos_destaque,
        get_diferenciais,
    )

    context = {
        "servicos_destaque": get_servicos_destaque(),
        "projetos_destaque": get_projetos_destaque(),
        "diferenciais": get_diferenciais(),
        "whatsapp_url": whatsapp_link(),
    }
    return render_template("pages/home.html", **context)


@main_bp.route("/sobre")
def sobre():
    """Página Sobre a empresa."""
    from core.services.content_service import get_missao_visao_valores

    context = {
        "mvvs": get_missao_visao_valores(),
        "whatsapp_url": whatsapp_link(),
    }
    return render_template("pages/sobre.html", **context)


@main_bp.route("/contato")
def contato():
    """Página de Contato."""
    context = {
        "whatsapp_url": whatsapp_link(),
    }
    return render_template("pages/contato.html", **context)
