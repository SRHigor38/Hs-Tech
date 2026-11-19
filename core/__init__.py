"""HS Tech — Núcleo da aplicação.

Application Factory: cria e configura a instância do Flask.
"""
from flask import Flask, render_template, request

from config import Config, get_config

# Importar modelos para registrar no SQLAlchemy
from core import models as core_models  # noqa: F401,F403


def create_app() -> Flask:
    """Cria a aplicação Flask com todas as configurações e registros.

    Returns:
        Flask: instância configurada da aplicação.
    """
    app = Flask(
        __name__,
        template_folder=str(Config.TEMPLATES_DIR),
        static_folder=str(Config.STATIC_DIR),
    )

    # Carrega configurações do ambiente ativo
    app.config.from_object(get_config())
    if app.config.get("TRUST_RENDER_PROXY"):
        # Apenas atrás do proxy confiável; não confia no cabeçalho de IP.
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=0, x_proto=1, x_host=0, x_port=0, x_prefix=0)

    from core.structured_logging import configure_logging
    configure_logging(app)

    # Garante que os diretórios necessários existam
    Config.ensure_directories()

    # Inicializa extensões antes do registro das rotas
    init_extensions(app)

    # Registra os blueprints
    from core.blueprints import register_blueprints
    register_blueprints(app)

    # Registra os error handlers
    register_error_handlers(app)

    # Registra os context processors (dados globais dos templates)
    register_context_processors(app)

    # Aplica headers de segurança em todas as respostas
    apply_security_headers(app)

    register_cli(app)
    register_publication_guard(app)

    return app


def apply_security_headers(app: Flask) -> None:
    """Aplica headers de segurança em todas as respostas HTTP."""
    headers = app.config.get("SECURITY_HEADERS", {})

    @app.after_request
    def add_security_headers(response):
        for header, value in headers.items():
            response.headers[header] = value
        if request.path.startswith("/admin") or request.path in {"/login", "/logout", "/contato"}:
            response.headers["Cache-Control"] = "no-store"
        return response


def register_error_handlers(app: Flask) -> None:
    """Registra os handlers de erro personalizados."""
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        try:
            return render_template("errors/500.html"), 500
        except Exception:
            # Não consultar o banco nem exibir detalhes se a própria página de erro falhar.
            return "Ocorreu um erro. Tente novamente mais tarde.", 500, {"Content-Type": "text/plain; charset=utf-8"}


def register_context_processors(app: Flask) -> None:
    """Injeta dados globais disponíveis em todos os templates."""
    from core.utils.helpers import current_year, empresa_config, whatsapp_link

    @app.context_processor
    def inject_globals():
        return {
            "ano_atual": current_year(),
            "empresa": empresa_config(),
            "whatsapp_url": whatsapp_link(),
        }


def init_extensions(app: Flask) -> None:
    """Inicializa as extensões do Flask.

    Futuro: SQLAlchemy, Migrate, LoginManager serão ativados aqui.
    """
    from core.extensions import load_extensions

    load_extensions(app)

def register_cli(app):
    import click
    from werkzeug.security import generate_password_hash
    from core.models import Administrador
    from core.extensions import db

    @app.cli.command("seed-services")
    def seed_services():
        """Cadastra o catálogo inicial apenas em banco sem serviços."""
        from core.models import Servico
        if Servico.query.first() is not None:
            raise click.ClickException("Já existem serviços. Nenhum registro foi alterado.")
        servicos = [
            ("sites-profissionais", "Sites profissionais", "Sites modernos, responsivos e personalizados para apresentar negócios e fortalecer sua presença digital.", "Layout responsivo\nPresença digital profissional"),
            ("landing-pages", "Landing pages", "Páginas estratégicas para apresentar produtos, serviços e campanhas.", "Comunicação focada\nPágina adaptada para celulares"),
            ("sistemas-web", "Sistemas web", "Sistemas personalizados para organizar informações, clientes, agendamentos e processos.", "Organização de informações\nProcessos adaptados ao negócio"),
            ("lojas-virtuais", "Lojas virtuais", "Soluções de comércio eletrônico para apresentar produtos e facilitar vendas online.", "Catálogo de produtos\nExperiência de compra online"),
            ("automacoes", "Automações", "Automatização de processos repetitivos e integração de funcionalidades digitais.", "Menos tarefas repetitivas\nIntegração de processos"),
            ("manutencao-evolucao-software", "Manutenção e evolução de software", "Correções, melhorias e novas funcionalidades em sites e sistemas.", "Correção de problemas\nEvolução de funcionalidades"),
        ]
        for slug, nome, descricao, beneficios in servicos:
            db.session.add(Servico(slug=slug, nome=nome, descricao=descricao, beneficios=beneficios, icone="code", status_publicacao="publicado"))
        db.session.commit()
        click.echo("Seis serviços iniciais cadastrados.")

    @app.cli.command("seed-demo-portfolio")
    def seed_demo_portfolio():
        """Cria rascunhos demonstrativos ausentes sem alterar registros existentes."""
        from core.models import Projeto
        examples = [
            ("demonstracao-barbearia", "Demonstração de barbearia", "Agendamentos e organização de horários em ambiente fictício.", "Agendamentos e serviços\nGestão demonstrativa"),
            ("demonstracao-personal-trainer", "Demonstração para Personal Trainer", "Exemplo de gestão de alunos e fichas de treino com dados fictícios.", "Alunos e fichas de treino\nHistórico de atividades"),
            ("demonstracao-ecommerce", "Demonstração de loja virtual", "Loja fictícia com catálogo e pedidos simulados sem pagamento.", "Catálogo e busca\nCarrinho e pedidos simulados\nProdutos e estoque fictícios"),
        ]
        created = 0
        for slug, nome, resumo, funcoes in examples:
            if Projeto.query.filter_by(slug=slug).first():
                continue
            db.session.add(Projeto(slug=slug, nome=nome, descricao_curta=resumo,
                                   descricao_completa=resumo, funcionalidades=funcoes,
                                   categoria="Demonstração", tecnologias="Python, Flask, SQLite",
                                   status_publicacao="rascunho", link_demo=None))
            created += 1
        db.session.commit()
        click.echo(f"{created} rascunho(s) criado(s); registros existentes foram preservados.")

    @app.cli.command("seed-dev-admin")
    @click.password_option("--password", prompt="Senha inicial de desenvolvimento", confirmation_prompt=True)
    def seed_dev_admin(password):
        """Cria administrador de teste somente se ainda não houver nenhum."""
        if not app.config.get("ALLOW_DEV_ADMIN"):
            raise click.ClickException("Disponível somente em desenvolvimento ou testes.")
        if Administrador.query.first() is not None:
            click.echo("Já existe administrador; nenhum dado foi alterado.")
            return
        if not 8 <= len(password) <= 1024:
            raise click.ClickException("A senha deve ter entre 8 e 1024 caracteres.")
        db.session.add(Administrador(usuario="admin", senha_hash=generate_password_hash(password), deve_trocar_senha=True))
        db.session.commit()
        click.echo("Administrador de desenvolvimento criado; troque a senha antes de publicar.")

    @app.cli.command("create-admin")
    @click.option("--usuario", prompt=True)
    @click.password_option("--password", prompt="Senha", confirmation_prompt=True)
    def create_admin(usuario, password):
        if not 12 <= len(password) <= 1024:
            raise click.ClickException("A senha deve ter entre 12 e 1024 caracteres.")
        if Administrador.query.first():
            raise click.ClickException("Já existe um administrador.")
        db.session.add(Administrador(usuario=usuario.strip(), senha_hash=generate_password_hash(password)))
        db.session.commit()
        click.echo("Administrador criado.")



def register_publication_guard(app):
    """Impede exibição pública em produção enquanto houver senha inicial ativa."""
    from flask import request, abort
    from core.models import Administrador
    @app.before_request
    def verificar_senha_inicial():
        if app.config.get("ALLOW_DEV_ADMIN") or app.testing:
            return None
        if request.endpoint in {"auth.login", "auth.logout", "auth.alterar_senha", "static"}:
            return None
        if Administrador.query.filter_by(deve_trocar_senha=True).first():
            abort(503, description="Configuração administrativa pendente.")

