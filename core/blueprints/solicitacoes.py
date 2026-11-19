"""HS Tech — Blueprint de Solicitações de Orçamento.

Rotas para gerenciar solicitações no painel administrativo.
"""
from datetime import datetime, timezone, timedelta
import re

from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, abort, jsonify
)
from flask_login import login_required
from core.extensions import db
from core.models import SolicitacaoOrcamento, Administrador, Projeto, Servico


solicitacoes_bp = Blueprint("solicitacoes", __name__)


@solicitacoes_bp.route("/dashboard")
@login_required
def dashboard():
    totais = {status: SolicitacaoOrcamento.query.filter_by(status=status).count() for status in ("novo", "em_analise", "em_negociacao", "aprovado", "recusado")}
    from collections import Counter
    dados = db.session.query(SolicitacaoOrcamento.data_recebimento, SolicitacaoOrcamento.tipo_solucao).all()
    meses = Counter(data.strftime("%Y-%m") for data, _ in dados if data)
    tipos = Counter(tipo or "Não informado" for _, tipo in dados)
    graficos = [
        ("Solicitações por mês", sorted(meses.items())),
        ("Solicitações por status", [("Novo", totais["novo"]), ("Em análise", totais["em_analise"]), ("Em negociação", totais["em_negociacao"]), ("Aprovado", totais["aprovado"]), ("Recusado", totais["recusado"])]),
        ("Tipos de solução", sorted(tipos.items(), key=lambda item: (-item[1], item[0])))
    ]
    return render_template("admin/dashboard.html", totais=totais, total=len(dados), projetos=Projeto.query.filter_by(status_publicacao="publicado").count(), servicos=Servico.query.count(), recentes=SolicitacaoOrcamento.query.order_by(SolicitacaoOrcamento.data_recebimento.desc()).limit(5).all(), graficos=graficos)


@solicitacoes_bp.route("/")
@login_required
def index():
    """Listar todas as solicitações de orçamento."""
    # Filtros
    status_filtro = request.args.get("status", type=str)
    data_inicio = request.args.get("data_inicio", type=str)
    data_fim = request.args.get("data_fim", type=str)
    busca = request.args.get("busca", type=str)

    query = SolicitacaoOrcamento.query

    # Filtro por status
    if status_filtro:
        query = query.filter(SolicitacaoOrcamento.status == status_filtro)

    # Filtro por período
    if data_inicio:
        try:
            from datetime import datetime, timezone
            dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
            query = query.filter(SolicitacaoOrcamento.data_recebimento >= dt_inicio)
        except ValueError:
            pass

    if data_fim:
        try:
            from datetime import datetime, timezone, timedelta
            dt_fim = datetime.strptime(data_fim, "%Y-%m-%d") + timedelta(days=1)
            query = query.filter(SolicitacaoOrcamento.data_recebimento < dt_fim)
        except ValueError:
            pass

    # Busca por nome
    if busca:
        query = query.filter(
            (SolicitacaoOrcamento.nome.ilike(f"%{busca}%")) |
            (SolicitacaoOrcamento.comercio.ilike(f"%{busca}%"))
        )

    # Ordenar por data mais recente
    query = query.order_by(SolicitacaoOrcamento.data_recebimento.desc())

    solicitacoes = query.all()

    # Contadores
    total = SolicitacaoOrcamento.query.count()
    novo = SolicitacaoOrcamento.query.filter_by(status="novo").count()
    analise = SolicitacaoOrcamento.query.filter_by(status="em_analise").count()
    negociacao = SolicitacaoOrcamento.query.filter_by(status="em_negociacao").count()
    aprovado = SolicitacaoOrcamento.query.filter_by(status="aprovado").count()
    recusado = SolicitacaoOrcamento.query.filter_by(status="recusado").count()

    context = {
        "solicitacoes": solicitacoes,
        "status_filtro": status_filtro,
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "busca": busca,
        "total": total,
        "novo": novo,
        "analise": analise,
        "negociacao": negociacao,
        "aprovado": aprovado,
        "recusado": recusado,
    }
    return render_template("admin/solicitacoes/index.html", **context)


@solicitacoes_bp.route("/<int:solicitacao_id>")
@login_required
def detalhes(solicitacao_id):
    """Visualizar detalhes de uma solicitação."""
    solicitacao = db.get_or_404(SolicitacaoOrcamento, solicitacao_id)
    numero = re.sub(r"[^0-9]", "", solicitacao.whatsapp or "")
    if len(numero) in (10, 11):
        numero = "55" + numero
    if not (numero.startswith("55") and len(numero) in (12, 13)):
        numero = None
    context = {
        "whatsapp_numero": numero,
        "solicitacao": solicitacao,
    }
    return render_template("admin/solicitacoes/detalhes.html", **context)


@solicitacoes_bp.route("/<int:solicitacao_id>/alterar-status", methods=["POST"])
@login_required
def alterar_status(solicitacao_id):
    """Alterar status da solicitação."""
    solicitacao = db.get_or_404(SolicitacaoOrcamento, solicitacao_id)
    status = request.form.get("status")

    # Validar status
    statuses_validos = ["novo", "em_analise", "em_negociacao", "aprovado", "recusado"]
    if status not in statuses_validos:
        flash("Status inválido.", "error")
        return redirect(url_for("solicitacoes.detalhes", solicitacao_id=solicitacao_id))

    solicitacao.status = status
    db.session.commit()

    flash(f"Status alterado para '{solicitacao.get_status_display()}'.", "success")
    return redirect(url_for("solicitacoes.detalhes", solicitacao_id=solicitacao_id))


@solicitacoes_bp.route("/<int:solicitacao_id>/adicionar-observacao", methods=["POST"])
@login_required
def adicionar_observacao(solicitacao_id):
    """Adicionar observação interna à solicitação."""
    solicitacao = db.get_or_404(SolicitacaoOrcamento, solicitacao_id)
    observacao = request.form.get("observacao", "").strip()

    if observacao:
        # Observações são armazenadas como uma lista que vai crescendo
        anterior = solicitacao.observacoes_internas or ""
        nova = f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} - Admin: {observacao}"
        solicitacao.observacoes_internas = "\n".join(filter(None, [anterior, nova]))

    db.session.commit()

    flash("Observação adicionada.", "success")
    return redirect(url_for("solicitacoes.detalhes", solicitacao_id=solicitacao_id))

@solicitacoes_bp.post("/<int:solicitacao_id>/excluir")
@login_required
def excluir(solicitacao_id):
    solicitacao = db.get_or_404(SolicitacaoOrcamento, solicitacao_id)
    db.session.delete(solicitacao)
    db.session.commit()
    flash("Solicitação excluída.", "success")
    return redirect(url_for("solicitacoes.index"))
