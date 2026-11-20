import os
import unittest
import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
os.environ['APP_ENV']='testing'
os.environ['SECRET_KEY']='teste-estatisticas'
os.environ['DATABASE_URL']='sqlite:///:memory:'
from app import app
from core.extensions import db
from core.models import AcessoPagina, Servico, Administrador
from core.services.textos_comerciais import atualizar_textos, NOVOS
from werkzeug.security import generate_password_hash

class AcessosTest(unittest.TestCase):
    def setUp(self):
        self.ctx=app.app_context(); self.ctx.push(); db.create_all()
        self.headers={'User-Agent':'Mozilla/5.0 Teste'}
    def tearDown(self):
        db.session.remove(); db.drop_all(); db.engine.dispose(); self.ctx.pop()
    def test_visitas_agrupadas_e_privacidade(self):
        c=app.test_client()
        self.assertEqual(c.get('/?email=nao-registrar', headers=self.headers).status_code,200)
        c.get('/', headers=self.headers); c.get('/contato', headers=self.headers)
        linhas=AcessoPagina.query.all()
        self.assertEqual(len(linhas),2)
        self.assertEqual(next(x for x in linhas if x.pagina=='Home').visualizacoes,2)
        self.assertEqual(len({x.visitante for x in linhas}),1)
        c.get('/sobre',headers={**self.headers,'DNT':'1'})
        c.get('/sobre',headers={**self.headers,'Sec-GPC':'1'})
        c.get('/admin/login',headers=self.headers)
        c.get('/sobre',headers={'User-Agent':'ExampleBot'})
        self.assertEqual(AcessoPagina.query.count(),2)
        c2=app.test_client(); c2.get('/',headers=self.headers)
        self.assertEqual(AcessoPagina.query.filter_by(pagina='Home').count(),2)
    def test_limpeza_e_estatisticas_vazias(self):
        hoje=datetime.now(ZoneInfo('America/Sao_Paulo')).date()
        db.session.add(AcessoPagina(data=hoje-timedelta(days=30),pagina='Home',visitante='a'*64,visualizacoes=1)); db.session.commit()
        app.test_client().get('/',headers=self.headers)
        self.assertEqual(AcessoPagina.query.filter_by(visitante='a'*64).count(),0)
    def test_textos_preservam_edicoes(self):
        db.session.add_all([Servico(slug='sites-profissionais',nome='Sites',descricao='Texto personalizado'),Servico(slug='automacoes',nome='Automações',descricao='Automatização de processos repetitivos e integração de funcionalidades digitais.')]); db.session.commit()
        self.assertEqual(atualizar_textos(),1)
        self.assertEqual(Servico.query.filter_by(slug='sites-profissionais').one().descricao,'Texto personalizado')
        self.assertIn('tarefas repetitivas',Servico.query.filter_by(slug='automacoes').one().descricao)
        self.assertEqual(set(NOVOS), {'sites-profissionais','landing-pages','sistemas-web','lojas-virtuais','automacoes','manutencao-evolucao-software'})
    def test_dashboard_requer_login_e_mostra_acessos(self):
        c=app.test_client(); c.get('/',headers=self.headers); c.get('/',headers=self.headers)
        self.assertEqual(c.get('/admin/dashboard').status_code,302)
        db.session.add(Administrador(usuario='teste',senha_hash=generate_password_hash('senha-forte-123'))); db.session.commit()
        login=c.get('/admin/login',headers=self.headers).get_data(as_text=True)
        csrf=re.search(r'name="csrf_token"[^>]*value="([^"]+)"',login).group(1)
        self.assertEqual(c.post('/admin/login',data={'csrf_token':csrf,'username':'teste','password':'senha-forte-123'},headers=self.headers).status_code,302)
        response=c.get('/admin/dashboard',headers=self.headers)
        self.assertEqual(response.status_code,200)
        self.assertIn('<strong>2</strong><span>visualizações · 1 visitantes estimados',response.get_data(as_text=True))
        self.assertEqual(AcessoPagina.query.count(),1)
