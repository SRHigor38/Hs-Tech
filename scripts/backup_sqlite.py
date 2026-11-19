"""Cria cópia consistente de SQLite em arquivo novo; não restaura nem sobrescreve."""
import argparse
import sqlite3
from contextlib import closing
from pathlib import Path

def backup(source, destination):
    source=Path(source).resolve(strict=True)
    destination=Path(destination).resolve()
    if not source.is_file() or source == destination:
        raise ValueError('Origem inválida.')
    # Criação exclusiva impede substituir backup ou banco por engano.
    with destination.open('xb'): pass
    try:
        with closing(sqlite3.connect(source.as_uri()+'?mode=ro',uri=True)) as src, closing(sqlite3.connect(destination)) as dst:
            src.backup(dst)
            if dst.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                raise ValueError('Falha na integridade do backup.')
    except Exception:
        # Preserve o arquivo parcial para investigação; não apague dados automaticamente.
        raise

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='Faz backup SQLite sem sobrescrever destino.')
    parser.add_argument('origem'); parser.add_argument('destino'); args=parser.parse_args()
    backup(args.origem,args.destino)
    print('Backup concluído e verificado.')
