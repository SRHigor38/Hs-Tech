"""Teste descartável com Redis simulado; não comprova Redis ou TLS reais."""
import os, subprocess, sys, tempfile, threading, time, urllib.request, socket
from pathlib import Path
import fakeredis

ROOT = Path(__file__).resolve().parents[1]

def run(code, env):
    result = subprocess.run([sys.executable, '-c', code], cwd=ROOT, env=env, capture_output=True, text=True, timeout=30)
    if result.returncode: raise RuntimeError('Processo isolado falhou: ' + result.stderr[-1500:])
    return result.stdout.strip()

with tempfile.TemporaryDirectory(dir=ROOT) as folder:
    folder=Path(folder).resolve(); database=folder/'descartavel.db'; static=folder/'static'; static.mkdir()
    server=fakeredis.TcpFakeServer(('127.0.0.1',0))
    thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
    env=os.environ.copy(); env.update(APP_ENV='production', SECRET_KEY='segredo-descartavel-apenas-para-testes-123456789', DATABASE_URL='sqlite:///'+database.as_posix(), RATELIMIT_STORAGE_URI='redis://127.0.0.1:'+str(server.server_address[1])+'/0', DEMO_STATIC=str(static), HS_LOG_DIR='')
    try:
        command=subprocess.run([sys.executable,'-m','flask','--app','app','db','upgrade'],cwd=ROOT,env=env,capture_output=True,text=True,timeout=30)
        if command.returncode: raise RuntimeError('Migração descartável falhou: '+command.stderr[-1500:])
        worker="""import re
from app import app
client=app.test_client()
res=client.get('/admin/login',base_url='https://localhost')
assert 'Secure' in res.headers.get('Set-Cookie','') and 'HttpOnly' in res.headers.get('Set-Cookie','')
token=re.search(rb'name="csrf_token"[^>]*value="([^"]+)"',res.data).group(1).decode()
values=[client.post('/admin/login',base_url='https://localhost',headers={'Referer':'https://localhost/admin/login'},data={'csrf_token':token,'username':'invalido','password':'teste'}).status_code for i in range(3)]
print(','.join(map(str,values)))
"""
        first=run(worker,env); second=run(worker,env)
        assert first=='200,200,200' and second=='200,200,429', (first,second)
        upload="""import io,os
from pathlib import Path
from config import Config
Config.STATIC_DIR=Path(os.environ['DEMO_STATIC'])
from app import app
from PIL import Image
from werkzeug.datastructures import FileStorage
from core.blueprints.admin_catalogo import guardar_imagem
buf=io.BytesIO(); Image.new('RGB',(5,5)).save(buf,'PNG'); buf.seek(0)
with app.app_context(): print(guardar_imagem(FileStorage(stream=buf,filename='teste.png')))
"""
        path=run(upload,env); assert (static / path).is_file()
        appcode="""from waitress import serve
from app import app
serve(app,host='127.0.0.1',port=int(__import__('os').environ['TEST_PORT']),threads=2)
"""
        with socket.socket() as sock: sock.bind(('127.0.0.1',0)); port=sock.getsockname()[1]
        env['TEST_PORT']=str(port)
        proc=subprocess.Popen([sys.executable,'-c',appcode],cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        try:
            for i in range(50):
                try:
                    with urllib.request.urlopen('http://127.0.0.1:'+str(port)+'/', timeout=2) as response: assert response.status==200
                    break
                except OSError: time.sleep(.1)
            else: raise RuntimeError('Servidor de teste não iniciou.')
        finally:
            proc.terminate(); proc.wait(timeout=10)
        assert database.is_file() and (static / path).is_file()
        print('OK: banco descartável, migração, servidor local, cookies seguros, upload persistente e limite entre dois processos com fakeredis.')
        print('Limitação: fakeredis é simulação; Redis real, TLS e infraestrutura externa não foram testados.')
    finally:
        server.shutdown(); server.server_close(); thread.join(timeout=5)
