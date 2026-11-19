"""Autenticação e acesso administrativo."""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, g
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from core.extensions import limiter, db
from core.models import Administrador

auth_bp = Blueprint("auth", __name__)
_DUMMY_PASSWORD_HASH = generate_password_hash(secrets.token_urlsafe(32))

@auth_bp.route("/login", methods=["GET", "POST"])
@auth_bp.route("/admin/login", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = Administrador.query.filter_by(usuario=username).first() if len(username) <= 50 else None
        password_valid = check_password_hash(user.senha_hash if user else _DUMMY_PASSWORD_HASH, password[:1024]) and len(password) <= 1024
        if user and password_valid:
            session.clear()
            g.pop("csrf_token", None)
            login_user(user, remember=False, fresh=True)
            if user.deve_trocar_senha and not current_app.config.get("ALLOW_DEV_ADMIN"):
                return redirect(url_for("auth.alterar_senha"))
            return redirect(url_for("auth.dashboard"))
        flash("Usuário ou senha inválidos.", "error")
    return render_template("auth/login.html")

@auth_bp.get("/admin/dashboard")
@login_required
def dashboard():
    from core.blueprints.solicitacoes import dashboard as dashboard_view
    return dashboard_view()

@auth_bp.route('/admin/alterar-senha', methods=['GET','POST'])
@login_required
@limiter.limit('5 per minute', methods=['POST'])
def alterar_senha():
    if request.method == 'POST':
        atual = request.form.get('atual', '')
        nova = request.form.get('nova', '')
        confirmacao = request.form.get('confirmacao', '')
        if not check_password_hash(current_user.senha_hash, atual):
            flash('A senha atual não confere.', 'error')
        elif not 12 <= len(nova) <= 1024:
            flash('A nova senha deve ter entre 12 e 1024 caracteres.', 'error')
        elif nova != confirmacao:
            flash('As novas senhas não conferem.', 'error')
        elif check_password_hash(current_user.senha_hash, nova):
            flash('Escolha uma senha diferente da atual.', 'error')
        else:
            current_user.senha_hash = generate_password_hash(nova)
            current_user.deve_trocar_senha = False
            db.session.commit()
            logout_user()
            session.clear()
            g.pop("csrf_token", None)
            flash('Senha atualizada. Entre novamente.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('auth/alterar_senha.html')

@auth_bp.post("/logout")
@auth_bp.post("/admin/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    g.pop("csrf_token", None)
    return redirect(url_for("auth.login"))
