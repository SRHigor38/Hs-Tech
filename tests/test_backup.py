import sqlite3, tempfile, unittest
from pathlib import Path
from scripts.backup_sqlite import backup

class BackupTest(unittest.TestCase):
    def test_copia_e_nao_sobrescreve(self):
        with tempfile.TemporaryDirectory(dir='.') as tmp:
            source=Path(tmp)/'origem.db'; target=Path(tmp)/'backup.db'
            conn=sqlite3.connect(source); conn.execute('CREATE TABLE exemplo(id INTEGER)'); conn.execute('INSERT INTO exemplo VALUES (42)'); conn.commit(); conn.close()
            backup(source,target)
            conn=sqlite3.connect(target); self.assertEqual(conn.execute('SELECT id FROM exemplo').fetchone()[0],42); conn.close()
            restore=Path(tmp)/'restaurado.db'; backup(target,restore)
            conn=sqlite3.connect(restore); self.assertEqual(conn.execute('SELECT id FROM exemplo').fetchone()[0],42); conn.close()
            with self.assertRaises(FileExistsError): backup(source,target)
            conn=sqlite3.connect(source); self.assertEqual(conn.execute('SELECT id FROM exemplo').fetchone()[0],42); conn.close()
