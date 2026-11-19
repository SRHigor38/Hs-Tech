"""Logs mínimos: não registram URL, IP, formulários, exceções ou cabeçalhos."""
import json
import logging
import re
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path
from flask import request

class SafeFormatter(logging.Formatter):
    def format(self, record):
        # Mensagens e exceções de bibliotecas podem conter parâmetros privados.
        event = getattr(record, 'safe_event', 'application_error' if record.levelno >= logging.ERROR else 'application_event')
        if event not in ('request', 'application_error', 'application_event'): event = 'application_event'
        data = {'timestamp': datetime.fromtimestamp(record.created, timezone.utc).isoformat(), 'level': record.levelname, 'event': event}
        if event == 'request':
            data['method'] = getattr(record, 'safe_method', '')
            data['endpoint'] = getattr(record, 'safe_endpoint', '')
            data['status'] = getattr(record, 'safe_status', 0)
        return json.dumps(data, ensure_ascii=False)

def configure_logging(app):
    logger = app.logger
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()
    directory = app.config.get('LOG_DIRECTORY')
    if directory:
        path = Path(directory); path.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(path / 'hstech.jsonl', maxBytes=app.config.get('LOG_MAX_BYTES', 10485760), backupCount=app.config.get('LOG_BACKUP_COUNT', 5), encoding='utf-8', delay=True)
    else:
        handler = logging.StreamHandler()
    handler.setFormatter(SafeFormatter())
    logger.addHandler(handler); logger.setLevel(logging.INFO); logger.propagate = False

    @app.after_request
    def log_request(response):
        if app.testing and not app.config.get('LOG_REQUESTS_IN_TESTS'):
            return response
        endpoint = request.endpoint or 'unknown'
        if not re.fullmatch(r'[A-Za-z0-9_.-]{1,100}', endpoint): endpoint = 'unknown'
        method = request.method if request.method in {'GET','POST','PUT','PATCH','DELETE','HEAD','OPTIONS'} else 'OTHER'
        app.logger.info('request', extra={'safe_event':'request', 'safe_method':method, 'safe_endpoint':endpoint, 'safe_status':response.status_code})
        return response
