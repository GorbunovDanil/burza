import json, threading, pathlib
DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
FAV_FILE = DATA / "favorites.json"
_lock = threading.Lock()

def load_favorites() -> list[str]:
    DATA.mkdir(exist_ok=True)
    if not FAV_FILE.exists():
        FAV_FILE.write_text("[]")
    with _lock, FAV_FILE.open() as f:
        return json.load(f)

def save_favorites(favs: list[str]) -> None:
    with _lock, FAV_FILE.open("w") as f:
        json.dump(sorted(set(favs)), f, indent=2)
