import io, os, re, tempfile, unittest
os.environ['APP_ENV']='testing'
os.environ['SECRET_KEY']='teste-configuracoes'
os.environ['DATABASE_URL']='sqlite:///:memory:'
from app import app
from core.extensions import db
from core.models import Administrador, EmpresaConfig
from werkzeug.security import generate_password_hash
from PIL import Image

def csrf(r): return re.search(rb'name="csrf_token"[^>]*value="([^"]+)"',r.data).group(1).decode()
class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.ctx=app.app_context(); self.ctx.push(); db.create_all(); app.config.update(TESTING=True, WTF_CSRF_ENABLED=True, RATELIMIT_ENABLED=False)
        db.session.add(Administrador(usuario='teste', senha_hash=generate_password_hash('senha-para-teste'))); db.session.commit()
        self.c=app.test_client(); self.tmp=tempfile.TemporaryDirectory(dir=os.getcwd()); self.static=app.static_folder; app.static_folder=self.tmp.name
    def tearDown(self):
        app.static_folder=self.static; self.tmp.cleanup(); db.session.remove(); db.drop_all(); db.engine.dispose(); self.ctx.pop()
    def dados(self):
        return {'nome':'Marca Teste','descricao':'Descrição institucional de teste','whatsapp':'5538999999999','email':'contato@example.com','instagram':'https://www.instagram.com/exemplo','linkedin':'','github':'https://github.com/exemplo','sobre_intro':'Apresentação de teste'}
    def login(self):
        r=self.c.get('/admin/login'); self.c.post('/admin/login', data={'csrf_token':csrf(r),'username':'teste','password':'senha-para-teste'})
    def test_autorizacao_validacao_e_integracao(self):
        self.assertEqual(self.c.get('/admin/configuracoes').status_code,302)
        self.assertEqual(self.c.post('/admin/configuracoes',data=self.dados()).status_code,400)
        self.login(); data=self.dados(); data['csrf_token']=csrf(self.c.get('/admin/configuracoes')); data['github']='javascript:alert(1)'
        self.assertEqual(self.c.post('/admin/configuracoes',data=data).status_code,200); self.assertEqual(EmpresaConfig.query.count(),0)
        data['github']='https://github.com/exemplo'; self.assertEqual(self.c.post('/admin/configuracoes',data=data).status_code,302)
        home=self.c.get('/').get_data(as_text=True); sobre=self.c.get('/sobre').get_data(as_text=True)
        self.assertIn('Marca Teste',home); self.assertIn('5538999999999',home); self.assertIn('contato@example.com',home); self.assertIn('Apresentação de teste',sobre)
        self.assertEqual(EmpresaConfig.query.filter_by(chave='nome').one().valor,'Marca Teste')
    def test_upload_valido_e_invalido(self):
        self.login(); data=self.dados(); data['csrf_token']=csrf(self.c.get('/admin/configuracoes')); data['logo']=(io.BytesIO(b'nao e imagem'), 'imagem.png')
        self.assertEqual(self.c.post('/admin/configuracoes',data=data,content_type='multipart/form-data').status_code,200); self.assertEqual(EmpresaConfig.query.count(),0)
        image=io.BytesIO(); Image.new('RGB',(8,8),'blue').save(image,'PNG'); image.seek(0)
        data=self.dados(); data['csrf_token']=csrf(self.c.get('/admin/configuracoes')); data['logo']=(image,'logo.png')
        self.assertEqual(self.c.post('/admin/configuracoes',data=data,content_type='multipart/form-data').status_code,302)
        logo=EmpresaConfig.query.filter_by(chave='logo').one().valor; self.assertTrue(os.path.isfile(os.path.join(self.tmp.name,logo))); self.assertIn(logo,self.c.get('/').get_data(as_text=True))
        img=io.BytesIO(); Image.new('RGB',(8,8),'red').save(img,'PNG'); img.seek(0)
        icon=io.BytesIO(); Image.new('RGB',(8,8),'white').save(icon,'PNG'); icon.seek(0)
        data=self.dados(); data['csrf_token']=csrf(self.c.get('/admin/configuracoes')); data['logo']=(img,'novo.png'); data['favicon']=(icon,'icone.png')
        self.assertEqual(self.c.post('/admin/configuracoes',data=data,content_type='multipart/form-data').status_code,302)
        novo=EmpresaConfig.query.filter_by(chave='logo').one().valor; favicon=EmpresaConfig.query.filter_by(chave='favicon').one().valor
        self.assertNotEqual(novo,logo); self.assertTrue(os.path.isfile(os.path.join(self.tmp.name,logo))); self.assertIn(favicon,self.c.get('/').get_data(as_text=True))

if __name__=='__main__': unittest.main()
