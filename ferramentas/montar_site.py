"""Monta o site público do LIMO a partir do pacote versionado."""
from pathlib import Path, PurePosixPath
import shutil
import zipfile

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / 'limo_publicacao.zip'
OUT = ROOT / 'publicacao'
with zipfile.ZipFile(PACKAGE) as archive:
    names = archive.namelist()
    required = {'index.html', 'jogo/index.html', 'jogo/js/main.js', 'jogo/js/build-profile.js'}
    if not required.issubset(names):
        raise SystemExit('Pacote incompleto: faltam arquivos essenciais')
    for item in archive.infolist():
        p = PurePosixPath(item.filename)
        if p.is_absolute() or '..' in p.parts or '\\' in item.filename or (item.external_attr >> 16) & 0o170000 == 0o120000:
            raise SystemExit(f'Caminho inseguro: {item.filename}')
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    archive.extractall(OUT)
print(f'Site montado: {len(names)} arquivos')
