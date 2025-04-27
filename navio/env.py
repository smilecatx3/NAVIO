import json
import os
import tempfile
from pathlib import Path

current_dir = Path(os.getcwd())

with open(current_dir/'config.json', encoding='utf-8') as f:
    config = json.load(f)

working_dir = Path(tempfile.mkdtemp())/'navio'/str(config['event_name'])
working_dir.mkdir(parents=True)
