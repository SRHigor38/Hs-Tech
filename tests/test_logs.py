import json, tempfile, unittest
from pathlib import Path
from flask import Flask
from core.structured_logging import configure_logging

class LoggingTest(unittest.TestCase):
    def test_rotacao_e_ausencia_dados_sensiveis(self):
        with tempfile.TemporaryDirectory(dir='.') as temp:
            app=Flask('teste_logs'); app.config.update(TESTING=True, LOG_REQUESTS_IN_TESTS=True, LOG_DIRECTORY=temp, LOG_MAX_BYTES=400, LOG_BACKUP_COUNT=3)
            configure_logging(app)
            @app.post('/teste')
            def teste():
                app.logger.error('segredo-formulario senha-supersecreta')
                return 'ok'
            client=app.test_client()
            for _ in range(4): client.post('/teste?dado=senha-supersecreta',data={'senha':'senha-supersecreta'})
            for h in app.logger.handlers: h.flush(); h.close()
            arquivos=list(Path(temp).glob('hstech.jsonl*')); self.assertGreater(len(arquivos),1)
            for path in arquivos:
                content=path.read_text(encoding='utf-8'); self.assertNotIn('senha-supersecreta',content); self.assertNotIn('segredo-formulario',content)
                for line in content.splitlines(): self.assertIn(json.loads(line)['event'],('request','application_error'))
