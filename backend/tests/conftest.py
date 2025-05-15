import os, sys
from pathlib import Path

# Tell Django where the settings are
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "burza_project.settings")

# Add *repo root* and *backend/* to sys.path
ROOT     = Path(__file__).resolve().parents[1]
BACKEND  = ROOT / "backend"
for p in (ROOT, BACKEND):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
