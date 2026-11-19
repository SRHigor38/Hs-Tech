"""Serviços públicos: catálogo inicial enquanto não houver cadastro publicado."""
from core.models import Servico

PADROES = [
    ("sites-profissionais", "Sites profissionais", "Sites que apresentam seu negócio e facilitam o contato com clientes."),
    ("landing-pages", "Landing pages", "Páginas focadas em apresentar uma oferta ou iniciativa."),
    ("sistemas-web", "Sistemas web", "Sistemas personalizados para organizar processos e informações."),
    ("lojas-virtuais", "Lojas virtuais", "Catálogos e lojas para apresentar e vender produtos online."),
    ("automacoes", "Automações", "Automação de tarefas repetitivas e integração de processos."),
    ("manutencao-e-evolucao", "Manutenção e evolução", "Melhorias e manutenção de sites e sistemas existentes."),
]

def servicos_publicos():
    cadastrados = Servico.query.filter_by(status_publicacao="publicado").order_by(Servico.ordem.asc(), Servico.nome.asc()).all()
    # Protege a apresentação comercial de dados antigos sem removê-los do banco.
    bloqueados = ("computador", "hardware", "formatação", "formatacao", "notebook", "montagem", "upgrade")
    digitais = [s for s in cadastrados if not any(termo in (s.nome or "").lower() for termo in bloqueados)]
    return digitais
