"""Testes isolados de importação e criação inicial de administrador."""
import os
import unittest
from unittest.mock import patch

os.environ['APP_ENV'] = 'testing'
os.environ['SECRET_KEY'] = 'teste-sincronizacao'
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
from app import app
from core.extensions import db
from core.models import Administrador, Projeto, Servico
from werkzeug.security import check_password_hash

class SincronizacaoTest(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context(); self.ctx.push(); db.create_all()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        db.session.remove(); db.drop_all(); db.engine.dispose(); self.ctx.pop()

    def test_catalogo_repetivel_sem_alterar_registros(self):
        db.session.add(Servico(slug='sites-profissionais', nome='Editado', status_publicacao='rascunho'))
        db.session.commit()
        self.assertEqual(self.runner.invoke(args=['importar-catalogo-inicial']).exit_code, 0)
        self.assertEqual(Servico.query.count(), 6)
        self.assertEqual(Servico.query.filter_by(slug='sites-profissionais').one().nome, 'Editado')
        projeto = Projeto.query.filter_by(slug='demonstracao-barbearia').one()
        self.assertEqual(projeto.status_publicacao, 'publicado')
        self.assertEqual(len(projeto.galeria), 4)
        self.assertIsNone(projeto.link_demo)
        self.assertTrue(all(p.status_publicacao == 'rascunho' for p in Projeto.query.filter(Projeto.slug != 'demonstracao-barbearia')))
        self.assertEqual(self.runner.invoke(args=['importar-catalogo-inicial']).exit_code, 0)
        self.assertEqual(Projeto.query.count(), 3)
        self.assertEqual(len(projeto.galeria), 4)

    def test_admin_env_nao_sobrescreve_nem_exibe_senha(self):
        with patch.dict(os.environ, {'HS_ADMIN_USER':'usuario-teste','HS_ADMIN_PASSWORD':'senha-de-teste-forte'}):
            resultado = self.runner.invoke(args=['bootstrap-admin-env'])
            self.assertEqual(resultado.exit_code, 0)
            self.assertNotIn('senha-de-teste-forte', resultado.output)
            usuario = Administrador.query.one()
            self.assertTrue(check_password_hash(usuario.senha_hash, 'senha-de-teste-forte'))
        with patch.dict(os.environ, {'HS_ADMIN_USER':'outro','HS_ADMIN_PASSWORD':'outra-senha-forte'}):
            self.assertEqual(self.runner.invoke(args=['bootstrap-admin-env']).exit_code, 0)
        self.assertEqual(Administrador.query.count(), 1)
        self.assertEqual(Administrador.query.one().usuario, 'usuario-teste')

    def test_admin_sem_credenciais_nao_cria_conta(self):
        with patch.dict(os.environ, {'HS_ADMIN_USER':'','HS_ADMIN_PASSWORD':''}):
            self.assertNotEqual(self.runner.invoke(args=['bootstrap-admin-env']).exit_code, 0)
        self.assertEqual(Administrador.query.count(), 0)
