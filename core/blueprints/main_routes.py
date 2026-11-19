"""HS Tech — Blueprint principal.

Rotas institucionais: Home, Sobre e Contato.
"""
from datetime import datetime, timezone

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf.csrf import CSRFProtect

from core.utils.helpers import whatsapp_link
from core.models import Projeto, Servico, EmpresaConfig, SolicitacaoOrcamento
from core.forms import ContatoForm
from core.services.public_services import servicos_publicos
from core.extensions import limiter

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """Página inicial."""
    # Buscar projetos e serviços do banco (apenas publicados)
    projetos = Projeto.query.filter_by(status_publicacao="publicado").order_by(Projeto.ordem.asc(), Projeto.data_cadastro.desc()).limit(6).all()
    servicos = servicos_publicos()

    # Buscar configuração da empresa
    config = EmpresaConfig.query.all()
    if config:
        config_dict = {}
        for c in config:
            config_dict[c.chave] = c.valor
    else:
        config_dict = {}

    context = {
        "servicos_destaque": servicos,
        "projetos_destaque": projetos,
        "whatsapp_url": whatsapp_link(),
        "empresa_config": config_dict,
    }
    return render_template("pages/home.html", **context)


@main_bp.route("/sobre")
def sobre():
    """Página Sobre a empresa."""
    config = EmpresaConfig.query.all()
    if config:
        config_dict = {}
        for c in config:
            config_dict[c.chave] = c.valor
    else:
        config_dict = {}

    # Dados padrão caso não haja config no banco
    defaults = {
        "nome": "HS Tech",
        "whatsapp": "5538991388394",
        "email": "hstech.py@gmail.com",
        "telefone": "(38) 99138-8394",
        "endereco": "Montes Claros - MG",
        "horario": "Atendimento via WhatsApp e e-mail",
        "instagram": "https://www.instagram.com/hs.tech.38",
        "linkedin": "",
        "github": "",
    }
    for k, v in defaults.items():
        if k not in config_dict:
            config_dict[k] = v

    # MVVs padrão
    mvvs = [
        {"titulo": "Atendimento Personalizado", "descricao": "Cada projeto é único. Ouvimos suas necessidades e entregamos uma solução sob medida para o seu objetivo.", "icone": "chat"},
        {"titulo": "Prazo e Qualidade", "descricao": "Compromisso com prazos combinados e qualidade impecável em cada entrega. Seu tempo é valioso.", "icone": "clock"},
        {"titulo": "Suporte Contínuo", "descricao": "Não sumimos após a entrega. Oferecemos suporte contínuo para garantir que tudo continue funcionando perfeitamente.", "icone": "shield"},
        {"titulo": "Tecnologia de Ponta", "descricao": "Utilizamos as melhores tecnologias e práticas de mercado para entregar soluções modernas, rápidas e seguras.", "icone": "rocket"},
    ]

    context = {
        "mvvs": mvvs,
        "empresa_config": config_dict,
        "whatsapp_url": whatsapp_link(),
    }
    return render_template("pages/sobre.html", **context)


@main_bp.route("/contato", methods=["GET", "POST"])
@limiter.limit("10 per hour", methods=["POST"])
def contato():
    """Página de Contato."""
    form = ContatoForm()

    if form.validate_on_submit():
        # Criar solicitação de orçamento
        solicitacao = SolicitacaoOrcamento(
            nome=form.nome.data,
            whatsapp=form.telefone.data,
            email=form.email.data,
            comercio=form.comercio.data,
            segmento=form.segmento.data,
            tipo_solucao=form.tipo_solucao.data,
            descricao=form.mensagem.data,
            data_recebimento=datetime.now(timezone.utc),
            status="novo",
            consentimento_data=datetime.now(timezone.utc),
            consentimento_versao="1",
        )
        from core.extensions import db
        db.session.add(solicitacao)
        db.session.commit()

        flash("Sua mensagem foi enviada com sucesso! Entraremos em contato rapidamente.", "success")
        return redirect(url_for("main.contato"))

    return render_template("pages/contato.html", form=form)

@main_bp.get("/privacidade")
def privacidade():
    """Informações sobre o tratamento dos dados enviados no orçamento."""
    return render_template("pages/privacidade.html")
