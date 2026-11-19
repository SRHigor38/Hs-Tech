import os, unittest
os.environ['APP_ENV']='testing'
os.environ['SECRET_KEY']='teste-portfolio'
os.environ['DATABASE_URL']='sqlite:///:memory:'
from app import app
from core.extensions import db
from core.models import Projeto

class PortfolioSeedTest(unittest.TestCase):
 def setUp(self):
  self.ctx=app.app_context(); self.ctx.push(); db.create_all()
 def tearDown(self):
  db.session.remove(); db.drop_all(); db.engine.dispose(); self.ctx.pop()
 def test_idempotente_e_rascunho(self):
  db.session.add(Projeto(slug='demonstracao-barbearia',nome='Existente',status_publicacao='publicado'));db.session.commit()
  for _ in range(2):
   r=app.test_cli_runner().invoke(args=['seed-demo-portfolio']); self.assertEqual(r.exit_code,0,r.output)
  self.assertEqual(Projeto.query.count(),3)
  original=Projeto.query.filter_by(slug='demonstracao-barbearia').one(); self.assertEqual(original.nome,'Existente'); self.assertEqual(original.status_publicacao,'publicado')
  for p in Projeto.query.filter(Projeto.slug!='demonstracao-barbearia').all():
   self.assertEqual(p.status_publicacao,'rascunho'); self.assertIsNone(p.link_demo); self.assertIsNone(p.imagem_principal)
