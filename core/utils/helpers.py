"""
HS Tech — Funções utilitárias.

Funções auxiliares usadas em rotas, templates e services.
"""

from datetime import datetime

from decouple import config


def current_year() -> int:
    """Retorna o ano atual (usado no rodapé e copyright)."""
    return datetime.now().year


def empresa_config() -> dict:
    """
    Retorna os dados da empresa carregados do .env.

    Esses dados ficam disponíveis em todos os templates
    através do context processor.
    """
    return {
        "nome": config("EMPRESA_NOME", default="HS Tech"),
        "whatsapp": config("EMPRESA_WHATSAPP", default="5538991388394"),
        "telefone": config("EMPRESA_TELEFONE", default="(38) 99138-8394"),
        "email": config("EMPRESA_EMAIL", default="hstech.py@gmail.com"),
        "endereco": config("EMPRESA_ENDERECO", default="Montes Claros - MG"),
        "horario": config("EMPRESA_HORARIO", default="Atendimento via WhatsApp e e-mail"),
        "instagram": config("EMPRESA_INSTAGRAM", default="https://www.instagram.com/hs.tech.38"),
        "linkedin": config("EMPRESA_LINKEDIN", default=""),
        "github": config("EMPRESA_GITHUB", default=""),
    }


def whatsapp_link(mensagem: str = "") -> str:
    """
    Gera o link do WhatsApp com mensagem pré-preenchida.

    Se nenhuma mensagem for fornecida, usa a mensagem padrão oficial.

    Args:
        mensagem: Texto da mensagem (opcional).

    Returns:
        str: URL completa do WhatsApp.
    """
    numero = config("EMPRESA_WHATSAPP", default="5538991388394")
    base = f"https://wa.me/{numero}"

    if not mensagem:
        mensagem = "Olá! Visitei o site da HS Tech e gostaria de solicitar um orçamento."

    from urllib.parse import quote

    return f"{base}?text={quote(mensagem)}"


def slugify(texto: str) -> str:
    """
    Converte um texto em slug amigável para URLs.

    Exemplo: "Desenvolvimento de Sites" → "desenvolvimento-de-sites"

    Futuro: usado em URLs de projetos, serviços e posts do blog.
    """
    import re
    from unicodedata import normalize

    texto = normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII")
    texto = re.sub(r"[^\w\s-]", "", texto).strip().lower()
    texto = re.sub(r"[-\s]+", "-", texto)
    return texto