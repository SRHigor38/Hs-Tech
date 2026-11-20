"""Medição própria de páginas públicas, sem IP nem parâmetros de URL."""
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from flask import current_app, request
from flask_login import current_user
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.exc import SQLAlchemyError

from core.extensions import db
from core.models import AcessoPagina

PAGINAS = {'main.home':'Home', 'main.sobre':'Sobre', 'main.contato':'Orçamento',
           'main.privacidade':'Privacidade', 'projetos.projetos':'Projetos',
           'projetos.detalhe':'Detalhes de projeto'}
COOKIE = 'hs_visita'

def registrar_visita(response):
    if (request.method != 'GET' or response.status_code != 200 or request.endpoint not in PAGINAS
            or current_user.is_authenticated or request.headers.get('DNT') == '1'
            or request.headers.get('Sec-GPC') == '1'):
        return response
    agente = request.headers.get('User-Agent', '').lower()
    if not agente or any(bot in agente for bot in ('bot', 'crawler', 'spider', 'render/')):
        return response
    token = request.cookies.get(COOKIE, '')
    novo = len(token) != 43 or not all(c.isalnum() or c in '-_' for c in token)
    if novo:
        token = secrets.token_urlsafe(32)
    identificador = hmac.new(current_app.secret_key.encode(), token.encode(), hashlib.sha256).hexdigest()
    hoje = datetime.now(ZoneInfo('America/Sao_Paulo')).date()
    try:
        tabela = AcessoPagina.__table__
        with db.engine.begin() as conexao:
            insert = pg_insert if conexao.dialect.name == 'postgresql' else sqlite_insert
            stmt = insert(tabela).values(data=hoje, pagina=PAGINAS[request.endpoint], visitante=identificador, visualizacoes=1)
            stmt = stmt.on_conflict_do_update(index_elements=['data','pagina','visitante'], set_={'visualizacoes': tabela.c.visualizacoes + 1})
            conexao.execute(stmt)
            conexao.execute(delete(tabela).where(tabela.c.data < hoje - timedelta(days=29)))
        if novo:
            response.set_cookie(COOKIE, token, max_age=30*24*60*60, httponly=True,
                                secure=current_app.config.get('SESSION_COOKIE_SECURE', False), samesite='Lax')
    except SQLAlchemyError:
        current_app.logger.warning('Falha ao registrar estatísticas de acesso.')
    return response
