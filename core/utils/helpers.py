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
    dados = {
        "nome": config("EMPRESA_NOME", default="HS Tech"),
        "whatsapp": config("EMPRESA_WHATSAPP", default="5538991388394"),
        "telefone": config("EMPRESA_TELEFONE", default="(38) 99138-8394"),
        "email": config("EMPRESA_EMAIL", default="hstech.py@gmail.com"),
        "endereco": config("EMPRESA_ENDERECO", default="Montes Claros - MG"),
        "horario": config("EMPRESA_HORARIO", default="Atendimento via WhatsApp e e-mail"),
        "instagram": config("EMPRESA_INSTAGRAM", default="https://www.instagram.com/hs.tech.38"),
        "linkedin": config("EMPRESA_LINKEDIN", default=""),
        "github": config("EMPRESA_GITHUB", default=""),
        "descricao": "Sites, sistemas, lojas virtuais e automações para o seu negócio.",
        "sobre_intro": "",
        "logo": "", "favicon": "",
    }
    from core.models import EmpresaConfig
    for item in EmpresaConfig.query.all():
        if item.chave in dados and item.valor is not None:
            dados[item.chave] = item.valor
    if not dados.get('sobre_intro'):
        dados['sobre_intro'] = f"{dados['nome']} desenvolve sites, sistemas e automações para ajudar negócios a evoluir no mundo digital."
    if dados.get('whatsapp'):
        dados['telefone'] = '+' + dados['whatsapp']
    return dados


def whatsapp_link(mensagem: str = "") -> str:
    """
    Gera o link do WhatsApp com mensagem pré-preenchida.

    Se nenhuma mensagem for fornecida, usa a mensagem padrão oficial.

    Args:
        mensagem: Texto da mensagem (opcional).

    Returns:
        str: URL completa do WhatsApp.
    """
    numero = empresa_config()["whatsapp"]
    base = f"https://wa.me/{numero}"

    if not mensagem:
        mensagem = f"Olá! Visitei o site da {empresa_config()['nome']} e gostaria de solicitar um orçamento."

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