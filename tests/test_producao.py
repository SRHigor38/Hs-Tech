import os, subprocess, sys, unittest

class ProducaoTest(unittest.TestCase):
    def verificar(self, **values):
        env=os.environ.copy(); env.update(APP_ENV='production', SECRET_KEY='segredo-de-teste-com-mais-de-32-caracteres', DATABASE_URL='sqlite:///temporario.db', RATELIMIT_STORAGE_URI='redis://localhost:6379/0'); env.update(values)
        return subprocess.run([sys.executable, '-c', 'from config import get_config; get_config()'],env=env,capture_output=True,text=True)
    def test_exige_chave_banco_e_limitador(self):
        self.assertNotEqual(self.verificar(SECRET_KEY='fraca').returncode,0)
        self.assertNotEqual(self.verificar(DATABASE_URL='').returncode,0)
        self.assertNotEqual(self.verificar(RATELIMIT_STORAGE_URI='memory://').returncode,0)
        self.assertEqual(self.verificar().returncode,0)

    def test_limite_de_tentativas_em_memoria(self):
        env=os.environ.copy(); env.update(APP_ENV='testing', SECRET_KEY='teste-de-limite', DATABASE_URL='sqlite:///:memory:', RATELIMIT_STORAGE_URI='memory://')
        script = """import re
from app import app
from core.extensions import db, limiter
with app.app_context():
 db.create_all(); limiter.reset(); c=app.test_client(); token=re.search(rb'name=\"csrf_token\"[^>]*value=\"([^\"]+)\"',c.get('/admin/login').data).group(1).decode()
 statuses=[c.post('/admin/login',data={'csrf_token':token,'username':'teste','password':'invalida'}).status_code for _ in range(6)]
 assert statuses[-1]==429, statuses
 db.session.remove(); db.drop_all(); db.engine.dispose()
"""
        result=subprocess.run([sys.executable,'-c',script],env=env,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
