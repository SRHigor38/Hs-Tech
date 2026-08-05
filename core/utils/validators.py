"""
HS Tech — Validadores.

Funções de validação de dados de entrada (server-side).
Nunca confiar apenas na validação do navegador.
"""

import re

# Padrões de validação
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
TELEFONE_REGEX = r"^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$"
NOME_REGEX = r"^[A-Za-zÀ-ÿ' ]{3,80}$"


def validar_email(email: str) -> bool:
    """
    Valida formato de e-mail.

    Args:
        email: E-mail a ser validado.

    Returns:
        True se o e-mail for válido, False caso contrário.
    """
    if not email or len(email) > 120:
        return False
    return bool(re.match(EMAIL_REGEX, email.strip()))


def validar_telefone(telefone: str) -> bool:
    """
    Valida telefone brasileiro (formato flexível).

    Aceita: (38) 99138-8394, 38991388394, 38 99138-8394

    Args:
        telefone: Telefone a ser validado.

    Returns:
        True se o telefone for válido, False caso contrário.
    """
    if not telefone:
        return False
    return bool(re.match(TELEFONE_REGEX, telefone.strip()))


def validar_nome(nome: str) -> bool:
    """
    Valida nome (apenas letras, acentos, apóstrofo e espaço).

    Args:
        nome: Nome a ser validado.

    Returns:
        True se o nome for válido, False caso contrário.
    """
    if not nome:
        return False
    return bool(re.match(NOME_REGEX, nome.strip()))


def validar_mensagem(mensagem: str, min_caracteres: int = 10) -> bool:
    """
    Valida tamanho da mensagem.

    Args:
        mensagem: Texto da mensagem.
        min_caracteres: Quantidade mínima de caracteres (padrão: 10).

    Returns:
        True se a mensagem for válida, False caso contrário.
    """
    if not mensagem:
        return False
    return len(mensagem.strip()) >= min_caracteres


def sanitizar_texto(texto: str) -> str:
    """
    Remove caracteres perigosos e normaliza espaços.

    Args:
        texto: Texto a ser sanitizado.

    Returns:
        str: Texto limpo.
    """
    if not texto:
        return ""
    texto = texto.strip()
    texto = re.sub(r"\s+", " ", texto)
    return texto


def extrair_telefone_digitos(telefone: str) -> str:
    """
    Extrai apenas os dígitos do telefone (usado no link do WhatsApp).

    Exemplo: "(38) 99138-8394" → "38991388394"

    Args:
        telefone: Telefone formatado.

    Returns:
        str: Apenas números.
    """
    return re.sub(r"\D", "", telefone)