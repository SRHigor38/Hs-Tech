"""Modelos de dados do HS Tech."""
from datetime import datetime, timezone

from core.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Configuracao(db.Model):
    """Configurações gerais da aplicação (armazenadas no banco)."""
    __tablename__ = 'configuracao'

    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.String(255), nullable=True)
    descricao = db.Column(db.String(255), nullable=True)
    data_atualizacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f'<Configuracao {self.chave}>'


class Administrador(UserMixin, db.Model):
    """Administradores do sistema."""
    __tablename__ = 'administrador'

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    deve_trocar_senha = db.Column(db.Boolean, nullable=False, default=False, server_default=db.false())
    email = db.Column(db.String(120), nullable=True)
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    ultimo_login = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Administrador {self.usuario}>'


class Projeto(db.Model):
    """Projetos desenvolvidos pela HS Tech."""
    __tablename__ = 'projeto'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    descricao_curta = db.Column(db.Text, nullable=True)
    descricao_completa = db.Column(db.Text, nullable=True)
    categoria = db.Column(db.String(50), nullable=True)
    imagem_principal = db.Column(db.String(200), nullable=True)
    problema = db.Column(db.Text, nullable=True)
    funcionalidades = db.Column(db.Text, nullable=True)
    beneficios = db.Column(db.Text, nullable=True)
    tecnologias = db.Column(db.Text, nullable=True)
    link_demo = db.Column(db.String(500), nullable=True)
    ordem = db.Column(db.Integer, nullable=False, default=0, server_default='0')
    status_publicacao = db.Column(db.String(20), default='rascunho', nullable=True)
    data_cadastro = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    data_atualizacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=True)

    def __repr__(self):
        return f'<Projeto {self.nome}>'


class ImagemProjeto(db.Model):
    """Imagem adicional vinculada a um projeto."""
    __tablename__ = 'imagem_projeto'
    id = db.Column(db.Integer, primary_key=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey('projeto.id', ondelete='CASCADE'), nullable=False, index=True)
    caminho = db.Column(db.String(200), nullable=False)
    projeto = db.relationship('Projeto', backref=db.backref('galeria', lazy='select', cascade='all, delete-orphan', order_by='ImagemProjeto.id'))


class AcessoPagina(db.Model):
    """Contagens por dia, página e identificador pseudônimo; sem IP."""
    __tablename__ = 'acesso_pagina'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, index=True)
    pagina = db.Column(db.String(50), nullable=False)
    visitante = db.Column(db.String(64), nullable=False)
    visualizacoes = db.Column(db.Integer, nullable=False, default=1)
    __table_args__ = (db.UniqueConstraint('data', 'pagina', 'visitante', name='uq_acesso_dia_pagina_visitante'),)


class Servico(db.Model):
    """Serviços oferecidos pela HS Tech."""
    __tablename__ = 'servico'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(80), unique=True, nullable=True)
    descricao = db.Column(db.Text, nullable=True)
    icone = db.Column(db.String(50), nullable=True)
    cor = db.Column(db.String(7), default='#0A84FF', nullable=True)
    beneficios = db.Column(db.Text, nullable=True)
    ordem = db.Column(db.Integer, nullable=False, default=0, server_default='0')
    status_publicacao = db.Column(db.String(20), default='publicado', nullable=True)
    data_cadastro = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f'<Servico {self.nome}>'


class EmpresaConfig(db.Model):
    """Configurações da empresa (podem substituir .env em produção)."""
    __tablename__ = 'empresa_config'

    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(50), unique=True, nullable=False)
    valor = db.Column(db.String(255), nullable=True)
    descricao = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<EmpresaConfig {self.chave}>'


class SolicitacaoOrcamento(db.Model):
    """Solicitações de orçamento recebidas pelo formulário público."""
    __tablename__ = 'solicitacao_orcamento'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    whatsapp = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    comercio = db.Column(db.String(120), nullable=True)
    segmento = db.Column(db.String(80), nullable=True)
    tipo_solucao = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    data_recebimento = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    status = db.Column(db.String(20), default='novo', nullable=True)  # novo, em_analise, em_negociacao, aprovado, recusado
    observacoes_internas = db.Column(db.Text, nullable=True)
    consentimento_data = db.Column(db.DateTime, nullable=True)
    consentimento_versao = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<SolicitacaoOrcamento {self.id}: {self.nome}>'

    def get_status_display(self):
        """Retorna descrição legível do status."""
        status_map = {
            'novo': 'Novo',
            'em_analise': 'Em Análise',
            'em_negociacao': 'Em Negociação',
            'aprovado': 'Aprovado',
            'recusado': 'Recusado',
        }
        return status_map.get(self.status, self.status)
