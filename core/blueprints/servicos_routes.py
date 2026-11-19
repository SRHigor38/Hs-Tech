"""Compatibilidade com o endereço anterior de serviços."""
from flask import Blueprint, redirect, url_for

servicos_bp = Blueprint("servicos", __name__)

@servicos_bp.get("/servicos")
def servicos():
    return redirect(url_for("main.home", _anchor="servicos"), code=301)
