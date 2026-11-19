import os, unittest
os.environ['APP_ENV']='testing'
os.environ['SECRET_KEY']='teste-portfolio-guia'
os.environ['DATABASE_URL']='sqlite:///:memory:'
from app import app
from core.extensions import db
from core.models import Projeto, ImagemProjeto

class PortfolioGuiaTest(unittest.TestCase):
 def setUp(self):
  self.ctx=app.app_context(); self.ctx.push(); db.create_all()
 def tearDown(self):
  db.session.remove(); db.drop_all(); db.engine.dispose(); self.ctx.pop()
 def test_galeria_legendas_ordem_e_sem_demo_interativa(self):
  p=Projeto(slug='teste-guia',nome='Sua Barbearia',categoria='Projeto demonstrativo',status_publicacao='publicado',link_demo='https://example.invalid/demo')
  p.galeria.append(ImagemProjeto(caminho='img/projetos/portfolio-demonstrativo/barbearia-servicos.png'))
  p.galeria.append(ImagemProjeto(caminho='img/projetos/portfolio-demonstrativo/barbearia-data.png'))
  db.session.add(p); db.session.commit()
  c=app.test_client(); response=c.get('/projetos/teste-guia'); self.assertEqual(response.status_code,200); html=response.get_data(as_text=True)
  self.assertIn('Projeto demonstrativo',html); self.assertLess(html.index('Escolha um serviço'),html.index('Selecione a data'))
  self.assertIn('Ampliar imagem 1',html); self.assertIn('Solicitar orçamento',html); self.assertNotIn('example.invalid',html)
  self.assertEqual(c.get('/projetos').status_code,200)

 def test_apresentacao_barbearia_usa_dados_editaveis_e_sem_demo(self):
  p=Projeto(slug='demonstracao-barbearia',nome='Sua Barbearia',categoria='Projeto demonstrativo',status_publicacao='publicado',descricao_curta='Texto editado no painel',descricao_completa='Sua barbearia organizada, seus agendamentos em um só lugar.',problema='Desafio editado',beneficios='Benefício editado',tecnologias='TECNOLOGIA OCULTA',link_demo='https://example.invalid/demo')
  p.galeria.append(ImagemProjeto(caminho='img/projetos/portfolio-demonstrativo/barbearia-passo-1.svg'))
  p.galeria.append(ImagemProjeto(caminho='img/projetos/portfolio-demonstrativo/barbearia-passo-2.svg'))
  p.galeria.append(ImagemProjeto(caminho='img/projetos/portfolio-demonstrativo/barbearia-passo-3.svg'))
  p.galeria.append(ImagemProjeto(caminho='img/projetos/portfolio-demonstrativo/barbearia-passo-4.svg'))
  db.session.add(p); db.session.commit()
  c=app.test_client(); html=c.get('/projetos/demonstracao-barbearia').get_data(as_text=True)
  self.assertIn('Texto editado no painel',html); self.assertIn('Desafio editado',html); self.assertIn('Benefício editado',html)
  self.assertIn('Sua barbearia organizada, seus agendamentos em um só lugar.',html)
  self.assertNotIn('TECNOLOGIA OCULTA',html); self.assertNotIn('example.invalid',html)
  titulos=['Conheça os serviços','Escolha a data e o horário','Confirme o agendamento','Acompanhe os agendamentos no painel']
  self.assertEqual(sorted(html.index(t) for t in titulos),[html.index(t) for t in titulos])
  self.assertEqual(html.count('class="case-image"'),4); self.assertIn('href="/contato"',html)
  self.assertIn('Muito mais que agendamentos',html)
  for titulo in ['Visão geral','Agendamentos','Serviços','Profissionais','Planos','Controle financeiro','Despesas e gastos','Configurações']:
   self.assertIn('<h3>'+titulo+'</h3>',html)
  self.assertEqual(html.count('class="case-admin-card"'),8)
  self.assertLess(html.index('Acompanhe os agendamentos no painel'),html.index('Muito mais que agendamentos'))
  self.assertLess(html.index('Muito mais que agendamentos'),html.index('Quer uma solução assim para o seu negócio?'))
  for item in p.galeria:
   response=c.get('/static/'+item.caminho); self.assertEqual(response.status_code,200); response.close()
