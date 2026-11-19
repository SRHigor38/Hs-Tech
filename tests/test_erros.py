import unittest
from flask import Flask, abort
from core import register_error_handlers

class ErrosTest(unittest.TestCase):
    def test_fallback_sem_dados_sensiveis(self):
        app=Flask('erro_isolado'); app.config['TESTING']=False; register_error_handlers(app)
        @app.context_processor
        def quebra(): raise RuntimeError('informacao-privada-de-teste')
        @app.get('/falha')
        def falha(): abort(500)
        response=app.test_client().get('/falha')
        self.assertEqual(response.status_code,500); self.assertIn('Tente novamente',response.get_data(as_text=True)); self.assertNotIn('informacao-privada-de-teste',response.get_data(as_text=True))
