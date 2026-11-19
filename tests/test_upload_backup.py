import tempfile, unittest
from pathlib import Path
from zipfile import ZipFile
from scripts.backup_uploads import backup, restore

class UploadBackupTest(unittest.TestCase):
    def test_backup_restauracao_e_preservacao(self):
        with tempfile.TemporaryDirectory(dir='.') as tmp:
            base=Path(tmp); source=base/'origem'; (source/'pasta').mkdir(parents=True); (source/'pasta/a.webp').write_bytes(b'imagem ficticia')
            archive=base/'arquivo.zip'; backup(source,archive); target=base/'restauracao'; restore(archive,target)
            self.assertEqual((target/'pasta/a.webp').read_bytes(),b'imagem ficticia')
            with self.assertRaises(FileExistsError): backup(source,archive)
            with self.assertRaises(ValueError): restore(archive,target)
            self.assertEqual((source/'pasta/a.webp').read_bytes(),b'imagem ficticia')
    def test_caminho_malicioso(self):
        with tempfile.TemporaryDirectory(dir='.') as tmp:
            base=Path(tmp); archive=base/'arquivo.zip'
            with ZipFile(archive,'w') as z: z.writestr('../escape.txt','nao')
            with self.assertRaises(ValueError): restore(archive,base/'destino')
            self.assertFalse((base/'escape.txt').exists())
            self.assertFalse((base/'destino').exists())
