"""Testes dos fluxos com banco de dados SQLite exclusivamente em memória."""
import os
os.environ['APP_ENV'] = 'testing'
os.environ['SECRET_KEY'] = 'chave-de-teste-isolado'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
import re
import unittest
from app import app
from core.extensions import db, limiter
from core.models import Administrador, SolicitacaoOrcamento, Projeto, Servico, ImagemProjeto
from werkzeug.security import generate_password_hash

def csrf(response):
    match = re.search(rb'name="csrf_token"[^>]*value="([^"]+)"', response.data)
    if not match:
        raise AssertionError('Token CSRF não encontrado')
    return match.group(1).decode()

class FluxoTest(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, WTF_CSRF_ENABLED=True, RATELIMIT_ENABLED=False)
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
        self.context = app.app_context(); self.context.push()
        db.create_all()
        db.session.add(Administrador(usuario='teste', senha_hash=generate_password_hash('senha-de-teste-123')))
        db.session.commit()
        limiter.reset()
        self.client = app.test_client()

    def tearDown(self):
        db.session.remove(); db.drop_all(); db.engine.dispose(); self.context.pop()

    def test_navegacao_e_projetos(self):
        from html.parser import HTMLParser
        class Links(HTMLParser):
            def __init__(self):
                super().__init__(); self.href = None; self.texto = ""; self.links = []
            def handle_starttag(self, tag, attrs):
                if tag == "a": self.href = dict(attrs).get("href"); self.texto = ""
            def handle_data(self, data):
                if self.href is not None: self.texto += data
            def handle_endtag(self, tag):
                if tag == "a" and self.href is not None:
                    self.links.append((self.texto.strip().lower(), self.href)); self.href = None
        self.assertEqual(self.client.get("/simulador").status_code, 404)
        for path in ["/", "/projetos", "/sobre", "/contato", "/privacidade"]:
            response = self.client.get(path); self.assertEqual(response.status_code, 200)
            content = response.get_data(as_text=True); links = Links(); links.feed(content)
            for label, href in links.links:
                if label in ("orçamento", "solicitar orçamento"): self.assertEqual(href, "/contato")
                if label == "contato": self.assertTrue(href.startswith("https://wa.me/"))
            self.assertNotIn("/simulador", content)
            self.assertNotIn("Explorar soluções", content)
            self.assertNotIn("Falar com a equipe", content)
            self.assertNotIn("Manutenção de Computadores", content)
        self.assertIn('Projetos e demonstrações serão publicados em breve', self.client.get('/projetos').get_data(as_text=True))
        db.session.add_all([Projeto(slug='p'+str(i), nome='Projeto '+str(i), categoria='Sistemas', status_publicacao='publicado') for i in range(8)] + [Projeto(slug='privado', nome='Projeto secreto', categoria='Privado', status_publicacao='rascunho')]); db.session.commit()
        primeira = self.client.get('/projetos').get_data(as_text=True)
        segunda = self.client.get('/projetos?pagina=2').get_data(as_text=True)
        self.assertIn('Próxima', primeira); self.assertIn('Anterior', segunda)
        self.assertNotIn('Projeto secreto', primeira); self.assertNotIn('Privado', primeira)
        detalhe = self.client.get('/projetos/p0'); self.assertEqual(detalhe.status_code, 200)
        self.assertNotIn('/simulador', detalhe.get_data(as_text=True))
        redirecionamento = self.client.get('/servicos')
        self.assertEqual(redirecionamento.status_code, 301)
        self.assertEqual(redirecionamento.headers['Location'], '/#servicos')
        servicos = self.client.get('/').get_data(as_text=True)
        self.assertIn('Novos serviços em breve', servicos)
        db.session.add_all([Servico(nome='Serviço publicado', slug='publicado', descricao='Descrição pública', beneficios='Benefício real', status_publicacao='publicado'), Servico(nome='Serviço privado',slug='privado',status_publicacao='rascunho')]); db.session.commit()
        servicos = self.client.get('/').get_data(as_text=True)
        self.assertIn('Serviço publicado', servicos)
        self.assertIn('Descrição pública', servicos)
        self.assertNotIn('Serviço privado', servicos)
        self.assertTrue(any('Projeto '+str(i) in servicos for i in range(8)))
        self.assertNotIn('Projeto secreto', servicos)

    def test_pagina_sobre(self):
        response = self.client.get('/sobre')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        for texto in ('Missão', 'Visão', 'Valores', 'Atendimento direto e personalizado', 'Desenvolvimento sob medida', 'Comunicação clara durante o projeto', 'Evolução de sites e sistemas'):
            self.assertIn(texto, html)
        self.assertEqual(html.count('class="about-icon"'), 3)
        self.assertIn('href="/contato" class="about-button"', html)
        self.assertNotIn('Falar com a equipe', html)
        self.assertNotIn('Falar com a HS Tech', html)

    def test_crud_catalogo_e_seguranca(self):
        import io
        c = self.client
        for path in ('/admin/projetos', '/admin/servicos', '/admin/projetos/novo', '/admin/servicos/novo'):
            self.assertEqual(c.get(path).status_code, 302)
        self.assertEqual(c.post('/admin/projetos/novo', data={}).status_code, 400)
        login = {'csrf_token':csrf(c.get('/login')), 'username':'teste', 'password':'senha-de-teste-123'}
        self.assertEqual(c.post('/login', data=login).status_code, 302)
        dashboard = c.get('/admin/dashboard'); self.assertEqual(dashboard.status_code, 200)
        self.assertNotIn('/simulador', dashboard.get_data(as_text=True))
        self.assertEqual(c.get('/admin/projetos').status_code, 200)
        self.assertEqual(c.get('/admin/servicos').status_code, 200)
        form = {'csrf_token':csrf(c.get('/admin/projetos/novo')), 'nome':'Projeto Teste', 'slug':'projeto-teste', 'categoria':'Web', 'descricao_curta':'Resumo', 'descricao_completa':'Detalhes', 'problema':'Questão', 'funcionalidades':'Cadastro', 'beneficios':'Organização', 'tecnologias':'Flask', 'link_demo':'', 'ordem':'2', 'status_publicacao':'rascunho'}
        self.assertEqual(c.post('/admin/projetos/novo', data=form).status_code, 302)
        self.assertEqual(c.get('/projetos/projeto-teste').status_code, 404)
        form['csrf_token'] = csrf(c.get('/admin/projetos/novo'))
        self.assertIn('slug já está em uso', c.post('/admin/projetos/novo', data=form).get_data(as_text=True))
        form['imagem'] = (io.BytesIO(b'arquivo falso'), 'teste.png')
        form['slug'] = 'projeto-upload'
        resposta = c.post('/admin/projetos/novo', data=form, content_type='multipart/form-data')
        self.assertIn('Arquivo de imagem inválido', resposta.get_data(as_text=True))
        self.assertIsNone(Projeto.query.filter_by(slug='projeto-upload').first())
        form.pop('imagem'); form['slug']='projeto-teste'; form['status_publicacao']='publicado'; form['nome']='Projeto Editado'
        form['csrf_token'] = csrf(c.get('/admin/projetos/1/editar'))
        self.assertEqual(c.post('/admin/projetos/1/editar', data=form).status_code, 302)
        self.assertEqual(c.get('/projetos/projeto-teste').status_code, 200)
        projeto = Projeto.query.filter_by(slug='projeto-teste').one()
        projeto.link_demo = 'https://example.invalid/demonstracao'; db.session.commit()
        detalhe = c.get('/projetos/projeto-teste').get_data(as_text=True)
        self.assertNotIn('https://example.invalid/demonstracao', detalhe)
        self.assertNotIn('Abrir demonstração', detalhe)
        self.assertIn('Projeto Editado', c.get('/').get_data(as_text=True))
        form['status_publicacao']='rascunho'
        self.assertEqual(c.post('/admin/projetos/1/editar', data=form).status_code, 302)
        self.assertEqual(c.get('/projetos/projeto-teste').status_code, 404)
        self.assertEqual(c.post('/admin/projetos/1/excluir').status_code, 400)
        self.assertEqual(c.post('/admin/projetos/1/excluir', data={'csrf_token': form['csrf_token']}).status_code, 302)
        self.assertEqual(Projeto.query.count(), 0)
        serv = {'csrf_token':csrf(c.get('/admin/servicos/novo')), 'nome':'Serviço Teste', 'slug':'servico-teste', 'descricao':'Descrição', 'beneficios':'Benefício', 'icone':'code', 'ordem':'1', 'status_publicacao':'rascunho'}
        self.assertEqual(c.post('/admin/servicos/novo', data=serv).status_code, 302)
        self.assertNotIn('Serviço Teste', c.get('/').get_data(as_text=True))
        serv['status_publicacao']='publicado'; serv['nome']='Serviço Editado'; serv['csrf_token']=csrf(c.get('/admin/servicos/1/editar'))
        self.assertEqual(c.post('/admin/servicos/1/editar', data=serv).status_code, 302)
        self.assertIn('Serviço Editado', c.get('/').get_data(as_text=True))
        serv['status_publicacao']='rascunho'
        self.assertEqual(c.post('/admin/servicos/1/editar', data=serv).status_code, 302)
        self.assertNotIn('Serviço Editado', c.get('/').get_data(as_text=True))
        self.assertEqual(c.post('/admin/servicos/1/excluir', data={'csrf_token':serv['csrf_token']}).status_code, 302)
        self.assertEqual(Servico.query.count(), 0)
        self.assertEqual(c.post('/logout',data={'csrf_token':serv['csrf_token']}).status_code, 302)
        self.assertEqual(c.get('/admin/projetos').status_code, 302)

    def test_upload_imagem_valida(self):
        import io, tempfile
        from PIL import Image
        from pathlib import Path
        c = self.client
        c.post('/login', data={'csrf_token':csrf(c.get('/login')), 'username':'teste', 'password':'senha-de-teste-123'})
        with tempfile.TemporaryDirectory(dir=os.getcwd()) as pasta:
            anterior = app.static_folder
            app.static_folder = pasta
            try:
                imagem = io.BytesIO(); Image.new('RGB', (12, 12), 'blue').save(imagem, format='PNG'); imagem.seek(0)
                dados = {'csrf_token':csrf(c.get('/admin/projetos/novo')), 'nome':'Projeto visual', 'slug':'projeto-visual', 'ordem':'0', 'status_publicacao':'publicado', 'imagem':(imagem,'foto.png')}
                resposta = c.post('/admin/projetos/novo',data=dados,content_type='multipart/form-data')
                self.assertEqual(resposta.status_code,302)
                projeto=Projeto.query.filter_by(slug='projeto-visual').one()
                self.assertTrue(projeto.imagem_principal.endswith('.webp'))
                self.assertTrue((Path(pasta)/projeto.imagem_principal).is_file())
                self.assertEqual(c.post('/admin/projetos/1/galeria', data={}).status_code, 400)
                galeria_token = csrf(c.get('/admin/projetos/1/galeria'))
                outra = io.BytesIO(); Image.new('RGB', (12,12), 'red').save(outra, format='PNG'); outra.seek(0)
                resposta = c.post('/admin/projetos/1/galeria', data={'csrf_token':galeria_token, 'imagem':(outra,'galeria.png')}, content_type='multipart/form-data')
                self.assertEqual(resposta.status_code, 302)
                imagem_galeria = ImagemProjeto.query.one()
                caminho = Path(pasta)/imagem_galeria.caminho
                self.assertTrue(caminho.is_file())
                self.assertIn(imagem_galeria.caminho, c.get('/projetos/projeto-visual').get_data(as_text=True))
                self.assertEqual(c.post('/admin/projetos/1/galeria/1/remover').status_code, 400)
                self.assertEqual(c.post('/admin/projetos/1/galeria/1/remover',data={'csrf_token':galeria_token}).status_code,302)
                self.assertEqual(ImagemProjeto.query.count(), 0)
                self.assertTrue(caminho.is_file())
                principal = Path(pasta) / projeto.imagem_principal
                dados_edicao = {'csrf_token':csrf(c.get('/admin/projetos/1/editar')), 'nome':'Projeto visual', 'slug':'projeto-visual', 'ordem':'0', 'status_publicacao':'publicado', 'remover_imagem':'y'}
                self.assertEqual(c.post('/admin/projetos/1/editar',data=dados_edicao).status_code,302)
                db.session.expire_all()
                self.assertIsNone(db.session.get(Projeto,1).imagem_principal)
                self.assertTrue(principal.is_file())
            finally:
                app.static_folder = anterior

    def test_acesso_separado_e_seed(self):
        c = self.client
        self.assertEqual(c.get('/').status_code,200)
        pagina=c.get('/admin/login').get_data(as_text=True)
        self.assertNotIn('Navegação principal', pagina)
        self.assertNotIn('WhatsApp', pagina)
        for path in ['/admin/dashboard','/admin/projetos','/admin/servicos','/admin/solicitacoes/']:
            r=c.get(path); self.assertEqual(r.status_code,302); self.assertTrue(r.location.startswith('/admin/login'))
        self.assertEqual(c.post('/admin/login',data={}).status_code,400)
        dados={'csrf_token':csrf(c.get('/admin/login')), 'username':'teste', 'password':'incorreta'}
        self.assertIn('inválidos',c.post('/admin/login',data=dados).get_data(as_text=True))
        anterior=Administrador.query.one().senha_hash
        runner=app.test_cli_runner()
        resultado=runner.invoke(args=['seed-dev-admin'],input='outra-senha-segura\noutra-senha-segura\n')
        self.assertEqual(resultado.exit_code,0)
        self.assertEqual(Administrador.query.count(),1)
        self.assertEqual(Administrador.query.one().senha_hash,anterior)
        dados['password']='senha-de-teste-123'
        resposta=c.post('/admin/login?next=https://example.invalid',data=dados)
        self.assertEqual(resposta.location,'/admin/dashboard')
        html=c.get('/admin/dashboard').get_data(as_text=True)
        self.assertNotIn('Navegação principal',html)
        token=csrf(c.get('/admin/dashboard'))
        self.assertEqual(c.post('/admin/logout',data={'csrf_token':token}).status_code,302)
        self.assertEqual(c.get('/admin/dashboard').status_code,302)

    def test_bloqueio_producao_senha_inicial(self):
        db.session.query(Administrador).delete(); db.session.commit()
        r=app.test_cli_runner().invoke(args=['seed-dev-admin'],input='senha-inicial-teste\nsenha-inicial-teste\n')
        self.assertEqual(r.exit_code,0)
        usuario=Administrador.query.one()
        self.assertTrue(usuario.deve_trocar_senha)
        self.assertNotEqual(usuario.senha_hash,'senha-inicial-teste')
        app.config.update(ALLOW_DEV_ADMIN=False,TESTING=False)
        try:
            self.assertEqual(self.client.get('/').status_code,503)
            token=csrf(self.client.get('/admin/login'))
            r=self.client.post('/admin/login',data={'csrf_token':token,'username':'admin','password':'senha-inicial-teste'})
            self.assertEqual(r.location,'/admin/alterar-senha')
            token=csrf(self.client.get('/admin/alterar-senha'))
            r=self.client.post('/admin/alterar-senha',data={'csrf_token':token,'atual':'senha-inicial-teste','nova':'senha-nova-segura-123','confirmacao':'senha-nova-segura-123'})
            self.assertEqual(r.status_code,302)
            db.session.expire_all()
            self.assertFalse(Administrador.query.one().deve_trocar_senha)
            self.assertEqual(self.client.get('/').status_code,200)
            r=app.test_cli_runner().invoke(args=['seed-dev-admin'],input='outra-senha-segura\noutra-senha-segura\n')
            self.assertNotEqual(r.exit_code,0)
        finally:
            app.config.update(ALLOW_DEV_ADMIN=True,TESTING=True)

    def test_validacao_contato(self):
        c = self.client
        dados = {'csrf_token': csrf(c.get('/contato')), 'nome': 'Pessoa Teste', 'telefone': '123', 'email': 'erro', 'tipo_solucao': 'sistema_web', 'mensagem': 'Teste'}
        resposta = c.post('/contato', data=dados)
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(SolicitacaoOrcamento.query.count(), 0)
        self.assertIn('telefone brasileiro válido', resposta.get_data(as_text=True))
        self.assertIn('necessário concordar', resposta.get_data(as_text=True))

    def test_fluxo_e_protecoes(self):
        c = self.client
        self.assertEqual(c.get('/admin/solicitacoes/').status_code, 302)
        self.assertEqual(c.post('/contato', data={}).status_code, 400)
        dados = {'csrf_token': csrf(c.get('/contato')), 'nome':'Pessoa Teste', 'telefone':'11999999999', 'email':'teste@example.com', 'tipo_solucao':'sistema_web', 'mensagem':'Mensagem fictícia', 'consentimento':'y'}
        self.assertEqual(c.post('/contato', data=dados).status_code, 302)
        self.assertEqual(SolicitacaoOrcamento.query.count(), 1)
        self.assertIn('enviada com sucesso', c.get('/contato').get_data(as_text=True))
        registro = SolicitacaoOrcamento.query.first()
        self.assertEqual(registro.status, 'novo')
        self.assertEqual(registro.consentimento_versao, '1')
        self.assertIsNotNone(registro.consentimento_data)
        login = {'csrf_token':csrf(c.get('/login')), 'username':'teste', 'password':'senha-de-teste-123'}
        self.assertEqual(c.post('/login', data=login).status_code, 302)
        painel = c.get('/admin/solicitacoes/dashboard')
        self.assertEqual(painel.status_code, 200)
        self.assertIn('Pessoa Teste', painel.get_data(as_text=True))
        self.assertIn('Solicitações por mês', painel.get_data(as_text=True))
        self.assertIn('sistema_web', painel.get_data(as_text=True))
        self.assertIn('Pessoa Teste', c.get('/admin/solicitacoes/?status=novo').get_data(as_text=True))
        self.assertNotIn('Pessoa Teste', c.get('/admin/solicitacoes/?status=aprovado').get_data(as_text=True))
        detalhes = c.get('/admin/solicitacoes/1')
        self.assertEqual(detalhes.status_code, 200)
        self.assertIn('https://wa.me/5511999999999', detalhes.get_data(as_text=True))
        token = csrf(detalhes)
        self.assertEqual(c.post('/admin/solicitacoes/1/alterar-status', data={'csrf_token':token,'status':'em_analise'}).status_code, 302)
        self.assertEqual(c.post('/admin/solicitacoes/1/adicionar-observacao', data={'csrf_token':token,'observacao':'nota fictícia'}).status_code, 302)
        db.session.expire_all(); registro = db.session.get(SolicitacaoOrcamento,1)
        self.assertEqual(registro.status, 'em_analise')
        self.assertIn('nota fictícia', registro.observacoes_internas)
        self.assertEqual(c.post('/admin/solicitacoes/1/excluir').status_code, 400)
        self.assertEqual(c.post('/admin/solicitacoes/1/excluir', data={'csrf_token':token}).status_code, 302)
        self.assertEqual(SolicitacaoOrcamento.query.count(), 0)

if __name__ == '__main__':
    unittest.main()
