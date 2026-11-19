"""Configuração institucional administrável sem migração ou alteração de dados anteriores."""
import re
from urllib.parse import urlsplit
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
from core.extensions import db
from core.models import EmpresaConfig
from core.utils.helpers import empresa_config
from core.blueprints.admin_catalogo import guardar_imagem

config_bp = Blueprint('configuracoes', __name__, url_prefix='/admin')
class ConfigForm(FlaskForm):
    nome = StringField('Nome da marca', validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField('Descrição institucional', validators=[DataRequired(), Length(max=255)])
    whatsapp = StringField('WhatsApp com DDI e DDD', validators=[DataRequired(), Length(min=12,max=13)])
    email = StringField('E-mail', validators=[DataRequired(), Email(), Length(max=120)])
    instagram = StringField('Instagram (URL HTTPS)', validators=[Optional(), Length(max=255)])
    linkedin = StringField('LinkedIn (URL HTTPS)', validators=[Optional(), Length(max=255)])
    github = StringField('GitHub (URL HTTPS)', validators=[Optional(), Length(max=255)])
    sobre_intro = TextAreaField('Texto de apresentação', validators=[Optional(), Length(max=255)])
    logo = FileField('Logo (PNG, JPEG ou WebP)', validators=[FileAllowed(['png','jpg','jpeg','webp'])])
    favicon = FileField('Ícone do site (PNG, JPEG ou WebP)', validators=[FileAllowed(['png','jpg','jpeg','webp'])])
    remover_logo = BooleanField('Usar logo padrão')
    remover_favicon = BooleanField('Usar ícone padrão')
    def validate_whatsapp(self, field):
        if not re.fullmatch(r'55[0-9]{10,11}', field.data or ''):
            raise ValidationError('Informe apenas números, com 55 e DDD.')
    def validate_instagram(self, field): self.validate_social(field, ('instagram.com','www.instagram.com'))
    def validate_linkedin(self, field): self.validate_social(field, ('linkedin.com','www.linkedin.com','br.linkedin.com'))
    def validate_github(self, field): self.validate_social(field, ('github.com','www.github.com'))
    def validate_social(self, field, hosts):
        if not field.data: return
        try:
            url = urlsplit(field.data)
            valid = url.scheme == 'https' and url.hostname in hosts and not url.username and not url.password and url.port in (None,443)
        except ValueError: valid = False
        if not valid:
            raise ValidationError('Informe uma URL HTTPS válida da rede correspondente.')

@config_bp.route('/configuracoes', methods=['GET','POST'])
@login_required
def index():
    values = empresa_config()
    form = ConfigForm(data=values)
    if form.validate_on_submit():
        for name in ('logo','favicon'):
            if getattr(form,name).data and getattr(form,'remover_'+name).data:
                getattr(form,name).errors.append('Escolha substituir ou restaurar o padrão.')
                return render_template('admin/configuracoes.html', form=form, empresa_atual=values)
        uploads = {}
        for name in ('logo','favicon'):
            if getattr(form,name).data:
                try: uploads[name] = guardar_imagem(getattr(form,name).data)
                except ValueError as exc:
                    getattr(form,name).errors.append(str(exc))
                    return render_template('admin/configuracoes.html', form=form, empresa_atual=values)
            elif getattr(form,'remover_'+name).data: uploads[name] = ''
        for key in ('nome','descricao','whatsapp','email','instagram','linkedin','github','sobre_intro'):
            uploads[key] = (getattr(form,key).data or '').strip()
        for key, value in uploads.items():
            row = EmpresaConfig.query.filter_by(chave=key).first()
            if row is None: row = EmpresaConfig(chave=key); db.session.add(row)
            row.valor = value
        db.session.commit()
        flash('Configurações atualizadas.', 'success')
        return redirect(url_for('configuracoes.index'))
    return render_template('admin/configuracoes.html', form=form, empresa_atual=values)
