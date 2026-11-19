import os, subprocess, sys, unittest
from config import normalizar_database_url
from core.extensions import client_limit_key
from app import app

class RenderTest(unittest.TestCase):
    def test_urls_postgres(self):
        self.assertEqual(normalizar_database_url('postgres://u:p@host/db'),'postgresql+psycopg://u:p@host/db')
        self.assertEqual(normalizar_database_url('postgresql://u:p@host/db'),'postgresql+psycopg://u:p@host/db')
        self.assertEqual(normalizar_database_url('sqlite:///:memory:'),'sqlite:///:memory:')
    def test_ip_confiavel_somente_configurado(self):
        original=app.config.get('TRUST_RENDER_CF_IP')
        try:
            app.config['TRUST_RENDER_CF_IP']=False
            with app.test_request_context('/',headers={'CF-Connecting-IP':'192.0.2.7'},environ_base={'REMOTE_ADDR':'127.0.0.1'}): self.assertEqual(client_limit_key(),'127.0.0.1')
            app.config['TRUST_RENDER_CF_IP']=True
            with app.test_request_context('/',headers={'CF-Connecting-IP':'192.0.2.7','X-Forwarded-For':'203.0.113.9'}): self.assertEqual(client_limit_key(),'192.0.2.7')
            with app.test_request_context('/',headers={'CF-Connecting-IP':'invalido'}): self.assertEqual(client_limit_key(),'render-header-ausente')
        finally: app.config['TRUST_RENDER_CF_IP']=original
    def test_sql_migracoes_postgres_offline(self):
        env=os.environ.copy(); env.update(APP_ENV='testing',SECRET_KEY='teste-somente-local',DATABASE_URL='postgresql://u:p@127.0.0.1:59999/descartavel')
        r=subprocess.run([sys.executable,'-m','flask','--app','app','db','upgrade','--sql'],env=env,capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stderr); self.assertIn('BOOLEAN DEFAULT false',r.stdout); self.assertIn('CREATE TABLE projeto',r.stdout)
    def test_https_atras_proxy_render(self):
        env=os.environ.copy(); env.update(APP_ENV='testing', SECRET_KEY='teste-somente-local', DATABASE_URL='sqlite:///:memory:', TRUST_RENDER_PROXY='true')
        script = "from app import app; app.add_url_rule('/probe',view_func=lambda: __import__('flask').request.scheme); c=app.test_client(); assert c.get('/probe',headers={'X-Forwarded-Proto':'https'}).get_data(as_text=True)=='https'"
        result=subprocess.run([sys.executable,'-c',script],env=env,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
    def test_yaml_render(self):
        try: import yaml
        except ImportError: self.skipTest('PyYAML necessário para esta verificação opcional')
        with open('render.yaml',encoding='utf-8') as f: config=yaml.safe_load(f)
        service=config['services'][0]; self.assertEqual(service['plan'],'0.5c-512mb'); self.assertEqual(service['autoDeployTrigger'],'off'); self.assertEqual(service['disk']['sizeGB'],1)
