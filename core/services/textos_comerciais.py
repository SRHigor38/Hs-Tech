"""Descrições iniciais atualizadas somente quando permanecem no texto original."""
import json
from pathlib import Path
from core.extensions import db
from core.models import Servico

NOVOS = {
    'sites-profissionais': 'Para negócios que precisam ser encontrados e transmitir confiança: apresente seus serviços e facilite o contato com clientes.',
    'landing-pages': 'Para quem quer divulgar uma oferta ou campanha: reúna as informações essenciais em uma página com um objetivo claro.',
    'sistemas-web': 'Para negócios que lidam com informações espalhadas: reúna dados e organize tarefas em um sistema feito para sua rotina.',
    'lojas-virtuais': 'Para quem vende produtos: apresente seu catálogo e ofereça uma forma prática de receber pedidos pela internet.',
    'automacoes': 'Para quem perde tempo com tarefas repetitivas: organize etapas do trabalho e reduza atividades feitas manualmente.',
    'manutencao-evolucao-software': 'Para quem já tem um site ou sistema: corrija problemas e adapte a solução às novas necessidades do negócio.',
}

def atualizar_textos():
    caminho = Path(__file__).resolve().parents[2] / 'scripts' / 'catalogo_inicial.json'
    iniciais = json.loads(caminho.read_text(encoding='utf-8'))['servicos']
    alterados = 0
    for inicial in iniciais:
        novo = NOVOS.get(inicial['slug'])
        atual = Servico.query.filter_by(slug=inicial['slug']).first()
        if novo and atual and atual.descricao == inicial['descricao']:
            atual.descricao = novo
            alterados += 1
    db.session.commit()
    return alterados
