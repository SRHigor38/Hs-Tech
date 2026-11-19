"""Gestão administrativa de projetos e serviços."""
from io import BytesIO
from pathlib import Path
from uuid import uuid4
from PIL import Image, UnidentifiedImageError, ImageOps
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from core.extensions import db
from core.forms import ProjetoForm, ServicoForm, GaleriaForm
from core.models import Projeto, Servico, ImagemProjeto

admin_catalogo_bp = Blueprint('admin_catalogo', __name__, url_prefix='/admin')


def guardar_imagem(arquivo):
    dados = arquivo.stream.read(4 * 1024 * 1024 + 1)
    if len(dados) > 4 * 1024 * 1024:
        raise ValueError('A imagem deve ter no máximo 4 MB.')
    try:
        with Image.open(BytesIO(dados)) as original:
            if original.format not in {'JPEG', 'PNG', 'WEBP'}:
                raise ValueError('Formato de imagem inválido.')
            if original.width * original.height > 20_000_000:
                raise ValueError('A imagem é grande demais.')
            original.verify()
        with Image.open(BytesIO(dados)) as original:
            imagem = ImageOps.exif_transpose(original)
            imagem.thumbnail((2400, 2400))
            if imagem.mode not in ('RGB', 'RGBA'):
                imagem = imagem.convert('RGBA' if 'transparency' in imagem.info else 'RGB')
            destino = Path(current_app.static_folder) / 'img' / 'projetos' / 'uploads'
            destino.mkdir(parents=True, exist_ok=True)
            nome = uuid4().hex + '.webp'
            imagem.save(destino / nome, format='WEBP', quality=85)
            return 'img/projetos/uploads/' + nome
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise ValueError('Arquivo de imagem inválido.') from exc


def listar(modelo, titulo, endpoint):
    query = modelo.query
    busca = request.args.get('busca', '').strip()
    status = request.args.get('status', '')
    if busca:
        query = query.filter(or_(modelo.nome.ilike(f'%{busca}%'), modelo.slug.ilike(f'%{busca}%')))
    if status in ('publicado', 'rascunho'):
        query = query.filter_by(status_publicacao=status)
    itens = query.order_by(modelo.ordem, modelo.nome).all()
    return render_template('admin/catalogo/lista.html', itens=itens, titulo=titulo, endpoint=endpoint, busca=busca, status=status)


def editar(modelo, form_cls, titulo, endpoint, item=None):
    form = form_cls(obj=item)
    if form.validate_on_submit():
        existente = modelo.query.filter_by(slug=form.slug.data).first()
        if existente is not None and (item is None or existente.id != item.id):
            form.slug.errors.append('Este slug já está em uso.')
        else:
            novo = item is None
            item = item or modelo()
            campos = ['nome', 'slug', 'descricao_curta', 'descricao_completa', 'categoria', 'problema', 'funcionalidades', 'beneficios', 'tecnologias', 'link_demo', 'ordem', 'status_publicacao'] if modelo is Projeto else ['nome', 'slug', 'descricao', 'beneficios', 'icone', 'ordem', 'status_publicacao']
            for campo in campos:
                valor = getattr(form, campo).data
                setattr(item, campo, valor.strip() if isinstance(valor, str) else valor)
            if modelo is Projeto and form.imagem.data and form.remover_imagem.data:
                form.imagem.errors.append('Escolha substituir ou remover a imagem, não os dois.')
                return render_template('admin/catalogo/form.html', form=form, titulo=titulo, endpoint=endpoint)
            if modelo is Projeto and form.remover_imagem.data:
                item.imagem_principal = None
            if modelo is Projeto and form.imagem.data:
                try:
                    item.imagem_principal = guardar_imagem(form.imagem.data)
                except ValueError as exc:
                    form.imagem.errors.append(str(exc))
                    return render_template('admin/catalogo/form.html', form=form, titulo=titulo, endpoint=endpoint)
            if novo:
                db.session.add(item)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                form.slug.errors.append('Este slug já está em uso.')
            else:
                flash('Alterações salvas com sucesso.', 'success')
                return redirect(url_for('admin_catalogo.' + endpoint))
    return render_template('admin/catalogo/form.html', form=form, titulo=titulo, endpoint=endpoint)


@admin_catalogo_bp.get('/projetos')
@login_required
def projetos(): return listar(Projeto, 'Projetos', 'projetos')

@admin_catalogo_bp.route('/projetos/novo', methods=['GET','POST'])
@login_required
def projeto_novo(): return editar(Projeto, ProjetoForm, 'Novo projeto', 'projetos')

@admin_catalogo_bp.route('/projetos/<int:item_id>/editar', methods=['GET','POST'])
@login_required
def projeto_editar(item_id): return editar(Projeto, ProjetoForm, 'Editar projeto', 'projetos', db.get_or_404(Projeto, item_id))

@admin_catalogo_bp.post('/projetos/<int:item_id>/excluir')
@login_required
def projeto_excluir(item_id):
    db.session.delete(db.get_or_404(Projeto, item_id)); db.session.commit(); flash('Projeto excluído.', 'success')
    return redirect(url_for('admin_catalogo.projetos'))

@admin_catalogo_bp.get('/servicos')
@login_required
def servicos(): return listar(Servico, 'Serviços', 'servicos')

@admin_catalogo_bp.route('/servicos/novo', methods=['GET','POST'])
@login_required
def servico_novo(): return editar(Servico, ServicoForm, 'Novo serviço', 'servicos')

@admin_catalogo_bp.route('/servicos/<int:item_id>/editar', methods=['GET','POST'])
@login_required
def servico_editar(item_id): return editar(Servico, ServicoForm, 'Editar serviço', 'servicos', db.get_or_404(Servico, item_id))

@admin_catalogo_bp.post('/servicos/<int:item_id>/excluir')
@login_required
def servico_excluir(item_id):
    db.session.delete(db.get_or_404(Servico, item_id)); db.session.commit(); flash('Serviço excluído.', 'success')
    return redirect(url_for('admin_catalogo.servicos'))


@admin_catalogo_bp.route('/projetos/<int:item_id>/galeria', methods=['GET', 'POST'])
@login_required
def projeto_galeria(item_id):
    projeto = db.get_or_404(Projeto, item_id)
    form = GaleriaForm()
    if form.validate_on_submit():
        try:
            caminho = guardar_imagem(form.imagem.data)
        except ValueError as exc:
            form.imagem.errors.append(str(exc))
        else:
            db.session.add(ImagemProjeto(projeto_id=projeto.id, caminho=caminho))
            db.session.commit()
            flash('Imagem adicionada à galeria.', 'success')
            return redirect(url_for('admin_catalogo.projeto_galeria', item_id=item_id))
    return render_template('admin/catalogo/galeria.html', projeto=projeto, form=form)


@admin_catalogo_bp.post('/projetos/<int:item_id>/galeria/<int:imagem_id>/remover')
@login_required
def projeto_galeria_remover(item_id, imagem_id):
    db.get_or_404(Projeto, item_id)
    imagem = ImagemProjeto.query.filter_by(id=imagem_id, projeto_id=item_id).first_or_404()
    db.session.delete(imagem)
    db.session.commit()
    flash('Imagem removida da galeria.', 'success')
    return redirect(url_for('admin_catalogo.projeto_galeria', item_id=item_id))
