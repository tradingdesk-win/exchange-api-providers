"""Offline structural validation; execution validation belongs to desktop runtime."""
import json
from pathlib import Path
from urllib.parse import urlsplit

root = Path(__file__).resolve().parents[1]

def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate key: {key}')
        result[key] = value
    return result

for path in sorted((root / 'providers').glob('*/adapter.json')):
    document = json.loads(path.read_text(), object_pairs_hook=unique)
    config = document['config']
    assert config['schemaVersion'] == 2
    adapter = config['adapter']
    assert urlsplit(adapter['origin']).scheme == 'https'
    assert adapter['walletType'] == 'SPOT'
    assert adapter['permissionWrites']
    for operation in adapter['operations'].values():
        assert operation['path'].startswith('/') and not operation['path'].startswith('//')
        assert operation['weight'] > 0
    print(f'OK {path.relative_to(root)}')
