"""Backup/restore de uploads para destinos novos, sem seguir links nem sobrescrever arquivos."""
import argparse
import shutil
import stat
from pathlib import Path, PurePosixPath
from zipfile import ZipFile, ZIP_DEFLATED

MAX_BYTES = 1024 * 1024 * 1024
MAX_FILES = 10000

def backup(source, archive):
    source = Path(source).resolve(strict=True)
    archive = Path(archive).resolve()
    if not source.is_dir() or source == archive or source in archive.parents:
        raise ValueError('Origem ou destino inválido.')
    files = []
    for p in source.rglob('*'):
        if p.is_symlink(): raise ValueError('Links simbólicos não são permitidos.')
        if p.is_file(): files.append(p)
        elif not p.is_dir(): raise ValueError('Tipo de arquivo não suportado.')
    if len(files) > MAX_FILES or sum(p.stat().st_size for p in files) > MAX_BYTES: raise ValueError('Limite de backup excedido.')
    with ZipFile(archive, mode='x', compression=ZIP_DEFLATED) as output:
        for p in files: output.write(p, p.relative_to(source).as_posix())

def restore(archive, destination):
    archive = Path(archive).resolve(strict=True); destination = Path(destination).resolve()
    if destination.exists() or destination == archive or destination in archive.parents: raise ValueError('Destino deve ser novo e fora do arquivo de backup.')
    with ZipFile(archive, 'r') as source:
        entries = source.infolist(); names = set(); total = 0
        if len(entries) > MAX_FILES: raise ValueError('Muitos arquivos.')
        for entry in entries:
            name = entry.filename
            parts = PurePosixPath(name).parts
            if not name or name.startswith('/') or '\\' in name or ':' in name or any(p in ('.','..') for p in parts): raise ValueError('Caminho inválido no backup.')
            key = name.casefold().rstrip('/')
            if key in names: raise ValueError('Caminho duplicado no backup.')
            names.add(key)
            if stat.S_ISLNK(entry.external_attr >> 16): raise ValueError('Link simbólico no backup.')
            total += entry.file_size
            if total > MAX_BYTES: raise ValueError('Backup excede o limite.')
        destination.mkdir(parents=True, exist_ok=False)
        for entry in entries:
            target = destination.joinpath(*PurePosixPath(entry.filename).parts)
            if entry.is_dir(): target.mkdir(parents=True,exist_ok=True); continue
            target.parent.mkdir(parents=True,exist_ok=True)
            with source.open(entry) as src, target.open('xb') as dst: shutil.copyfileobj(src,dst)

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Cópia e restauração de uploads sem sobrescrita.')
    parser.add_argument('operacao', choices=['backup','restore']); parser.add_argument('origem'); parser.add_argument('destino')
    args=parser.parse_args()
    (backup if args.operacao == 'backup' else restore)(args.origem,args.destino)
    print('Operação concluída.')
