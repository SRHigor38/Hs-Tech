"""
Configurações do projeto HS Tech.

Separa as configurações por ambiente (desenvolvimento, produção e testes)
para que o projeto possa crescer sem precisar ser reestruturado.
"""

from pathlib import Path
from decouple import config




def normalizar_database_url(url):
    """Usa psycopg 3 para URLs PostgreSQL comuns de provedores."""
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://"):]
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://"):]
    return url

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
    SQLALCHEMY_DATABASE_URI = normalizar_database_url(config(
        "DATABASE_URL",
        default=f"sqlite:///{INSTANCE_DIR / 'hs_tech.db'}",
    ))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Sessão
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    RATELIMIT_STORAGE_URI = config("RATELIMIT_STORAGE_URI", default="memory://")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    TRUST_RENDER_PROXY = config("TRUST_RENDER_PROXY", default=False, cast=bool)
    TRUST_RENDER_CF_IP = config("TRUST_RENDER_CF_IP", default=False, cast=bool)
    LOG_DIRECTORY = config("HS_LOG_DIR", default="")
    LOG_MAX_BYTES = 10 * 1024 * 1024
    LOG_BACKUP_COUNT = 5

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
    ALLOW_DEV_ADMIN = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Configurações do ambiente de produção."""

    DEBUG = False
    ALLOW_DEV_ADMIN = False
    SESSION_COOKIE_SECURE = True
    PREFERRED_URL_SCHEME = "https"

    # Em produção, exige uma SECRET_KEY forte definida via variável de ambiente
    SECRET_KEY = config("SECRET_KEY", default="")
    RATELIMIT_STORAGE_URI = config("RATELIMIT_STORAGE_URI", default="")


class TestingConfig(Config):
    """Configurações do ambiente de testes."""

    TESTING = True
    ALLOW_DEV_ADMIN = True
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
    if env not in CONFIG_MAP:
        raise RuntimeError("APP_ENV inválido: use development, testing ou production.")
    if env == "production":
        if len(ProductionConfig.SECRET_KEY) < 32:
            raise RuntimeError("SECRET_KEY deve ter pelo menos 32 caracteres em produção.")
        if not ProductionConfig.RATELIMIT_STORAGE_URI.startswith(("redis://", "rediss://")):
            raise RuntimeError("Configure RATELIMIT_STORAGE_URI compartilhado (Redis) em produção.")
        if not config("DATABASE_URL", default=""):
            raise RuntimeError("Configure DATABASE_URL persistente em produção.")
    return CONFIG_MAP[env]