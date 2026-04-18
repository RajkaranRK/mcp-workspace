import os
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORIES_ROOT = Path(
    os.getenv("REPOSITORIES_ROOT", str(DEFAULT_ROOT))
).resolve()
