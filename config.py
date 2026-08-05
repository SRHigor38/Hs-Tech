"""
Configurações do projeto HS Tech.

Separa as configurações por ambiente (desenvolvimento, produção e testes)
para que o projeto possa crescer sem precisar ser reestruturado.
"""

from pathlib import Path
from decouple import config


# Caminho base do projeto (raiz)
BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Configurações base compartilhadas por todos os ambientes."""

    # Segurança
    SECRET_KEY = config("SECRET_KEY", default="dev-secret-key-change-in-production")

    # Flask
    DEBUG = False
    TESTING = False

    # Caminhos
    BASE_DIR = BASE_DIR
    INSTANCE_DIR = BASE_DIR / "instance"
    DATABASE_DIR = BASE_DIR / "database"
    STATIC_DIR = BASE_DIR / "static"
    TEMPLATES_DIR = BASE_DIR / "templates"
    UPLOAD_DIR = BASE_DIR / "uploads"

    # Banco de dados (futuro - preparado para ativação)
    SQLALCHEMY_DATABASE_URI = config(
        "DATABASE_URL",
        default=f"sqlite:///{INSTANCE_DIR / 'hs_tech.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Sessão
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Ferramentas de segurança
    PREFERRED_URL_SCHEME = "http"

    # Headers de segurança padrão (aplicados em todos os ambientes)
    SECURITY_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    }

    @staticmethod
    def ensure_directories():
        """Garante que os diretórios necessários existam."""
        directories = [
            Config.INSTANCE_DIR,
            Config.DATABASE_DIR,
            Config.DATABASE_DIR / "backup",
            Config.UPLOAD_DIR,
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """Configurações do ambiente de desenvolvimento."""

    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Configurações do ambiente de produção."""

    DEBUG = False
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = "https"

    # Em produção, exige uma SECRET_KEY forte definida via variável de ambiente
    SECRET_KEY = config("SECRET_KEY")


class TestingConfig(Config):
    """Configurações do ambiente de testes."""

    TESTING = True
    DEBUG = True
    SESSION_COOKIE_SECURE = False


# Mapeamento de ambientes
CONFIG_MAP = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config():
    """Retorna a classe de configuração conforme o ambiente ativo."""
    env = config("APP_ENV", default="development")
    return CONFIG_MAP.get(env, DevelopmentConfig)