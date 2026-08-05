"""
HS Tech — Ponto de entrada da aplicação.

Executa o servidor de desenvolvimento do Flask.
Em produção, o Gunicorn importa `app` deste módulo.
"""

import os

from dotenv import load_dotenv

from core import create_app

# Carrega variáveis de ambiente do arquivo .env (apenas local/dev)
load_dotenv()

app = create_app()

if __name__ == "__main__":
    # Configurações do servidor de desenvolvimento
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))

    # DEBUG: ativo apenas em desenvolvimento (APP_ENV=development)
    debug = os.getenv("APP_ENV", "development") == "development"

    app.run(host=host, port=port, debug=debug)