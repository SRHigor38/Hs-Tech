"""HS Tech — Blueprint de Projetos.

Rota da página de portfólio (projetos).
"""
from flask import Blueprint, render_template, request

from core.extensions import db
from core.models import Projeto
from core.utils.helpers import whatsapp_link

projetos_bp = Blueprint("projetos", __name__)


@projetos_bp.route("/projetos")
def projetos():
    """Página de projetos (portfólio)."""
    # Buscar projetos publicados
    pagina = request.args.get('pagina', 1, type=int)
    categoria_filtro = request.args.get('categoria', None)

    query = Projeto.query.filter_by(status_publicacao="publicado")

    if categoria_filtro:
        query = query.filter_by(categoria=categoria_filtro)

    projetos = query.order_by(Projeto.ordem.asc(), Projeto.data_cadastro.desc()).paginate(
        page=pagina, per_page=6, error_out=False
    )

    categorias = db.session.query(Projeto.categoria).filter_by(status_publicacao="publicado").distinct().all()
    categorias = [c[0] for c in categorias if c[0]]  # Remover Nones

    context = {
        "projetos": projetos,
        "categorias": categorias,
        "categoria_filtro": categoria_filtro,
        "whatsapp_url": whatsapp_link(),
    }
    return render_template("pages/projetos.html", **context)

@projetos_bp.get('/projetos/<slug>')
def detalhe(slug):
    projeto = Projeto.query.filter_by(slug=slug, status_publicacao="publicado").first_or_404()
    from core.services.portfolio_guia import LEGENDAS
    template = "pages/projeto_barbearia.html" if projeto.slug == "demonstracao-barbearia" else "pages/projeto_detalhe.html"
    return render_template(template, projeto=projeto, legendas=LEGENDAS)
