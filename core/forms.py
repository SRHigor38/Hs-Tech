"""Formulários do HS Tech."""
import re
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, EmailField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError

try:
    from wtforms.fields import SelectChoice
except ImportError:
    SelectChoice = None

def select_choices(items):
    return [SelectChoice(value=value, label=label) for value, label in items] if SelectChoice else items


class ContatoForm(FlaskForm):
    """Formulário de contato público."""

    nome = StringField("Nome completo", validators=[DataRequired(message="Nome é obrigatório"), Length(max=100)])
    email = EmailField("E-mail", validators=[DataRequired(message="E-mail é obrigatório"), Email(message="E-mail inválido"), Length(max=100)])
    telefone = StringField("WhatsApp", validators=[DataRequired(message="Telefone é obrigatório"), Length(max=20)])
    comercio = StringField("Nome do negócio ou empresa", validators=[Optional(), Length(max=100)])
    segmento = StringField("Segmento do negócio", validators=[Optional(), Length(max=50)])
    tipo_solucao = SelectField("Tipo de solução desejada", choices=select_choices([
        ("", "Selecione o tipo de solução"),
        ("site_profissional", "Site profissional"),
        ("landing_page", "Landing page"),
        ("sistema_web", "Sistema web"),
        ("e-commerce", "Loja virtual"),
        ("automacao", "Automação"),
        ("manutencao", "Manutenção ou evolução de software"),
        ("outro", "Outro"),
    ]), validators=[DataRequired(message="Tipo de solução é obrigatório")])
    consentimento = BooleanField("Concordo com o uso dos dados informados para responder a esta solicitação de orçamento.", validators=[DataRequired(message="É necessário concordar para enviar.")])
    def validate_telefone(self, field):
        numero = re.sub(r"[^0-9]", "", field.data or "")
        if not (len(numero) in (10, 11) or (len(numero) in (12, 13) and numero.startswith("55"))):
            raise ValidationError("Informe um telefone brasileiro válido com DDD.")

    mensagem = TextAreaField("Descrição do projeto", validators=[DataRequired(message="Mensagem é obrigatória"), Length(max=1000)])

from flask_wtf.file import FileField, FileAllowed
from wtforms import IntegerField
from wtforms.validators import NumberRange, Regexp, URL

class ProjetoForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(max=120)])
    slug = StringField("Slug", validators=[DataRequired(), Length(max=80), Regexp(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", message="Use letras minúsculas, números e hífens.")])
    categoria = StringField("Categoria", validators=[Optional(), Length(max=50)])
    descricao_curta = TextAreaField("Descrição curta", validators=[Optional(), Length(max=500)])
    descricao_completa = TextAreaField("Descrição completa", validators=[Optional(), Length(max=10000)])
    problema = TextAreaField("Problema resolvido", validators=[Optional(), Length(max=5000)])
    funcionalidades = TextAreaField("Funcionalidades (uma por linha)", validators=[Optional(), Length(max=5000)])
    beneficios = TextAreaField("Benefícios (um por linha)", validators=[Optional(), Length(max=5000)])
    tecnologias = StringField("Tecnologias (separadas por vírgula)", validators=[Optional(), Length(max=500)])
    link_demo = StringField("Link de demonstração", validators=[Optional(), Length(max=500), URL(require_tld=False)])
    imagem = FileField("Imagem principal (PNG, JPEG ou WebP)", validators=[FileAllowed(['jpg','jpeg','png','webp'], 'Envie PNG, JPEG ou WebP.')])
    remover_imagem = BooleanField("Remover a imagem principal atual")
    ordem = IntegerField("Ordem de exibição", default=0, validators=[NumberRange(min=0, max=100000)])
    status_publicacao = SelectField("Publicação", choices=select_choices([('rascunho','Rascunho'),('publicado','Publicado')]), validators=[DataRequired()])

    def validate_link_demo(self, field):
        if field.data and not field.data.lower().startswith(('https://', 'http://')):
            raise ValidationError('Use um link HTTP ou HTTPS.')

class ServicoForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(max=100)])
    slug = StringField("Slug", validators=[DataRequired(), Length(max=80), Regexp(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", message="Use letras minúsculas, números e hífens.")])
    descricao = TextAreaField("Descrição", validators=[Optional(), Length(max=5000)])
    beneficios = TextAreaField("Benefícios (um por linha)", validators=[Optional(), Length(max=5000)])
    icone = SelectField("Ícone", choices=select_choices([('code','Código'),('cpu','Sistema'),('zap','Automação')]))
    ordem = IntegerField("Ordem de exibição", default=0, validators=[NumberRange(min=0,max=100000)])
    status_publicacao = SelectField("Publicação", choices=select_choices([('rascunho','Rascunho'),('publicado','Publicado')]), validators=[DataRequired()])


class GaleriaForm(FlaskForm):
    imagem = FileField("Imagem da galeria (PNG, JPEG ou WebP)", validators=[DataRequired(), FileAllowed(['jpg','jpeg','png','webp'], 'Envie PNG, JPEG ou WebP.')])
