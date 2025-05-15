import json
from pathlib import Path

import pytest

from api.files import load_favorites, save_favorites, FAV_FILE, DATA

def test_roundtrip(tmp_path, monkeypatch):
    # Redirect DATA dir and the precomputed FAV_FILE
    monkeypatch.setattr("api.files.DATA", tmp_path, raising=True)
    monkeypatch.setattr("api.files.FAV_FILE", tmp_path / "favorites.json", raising=True)

    # Save with a duplicate to test dedupe+sort
    save_favorites(["MSFT", "AAPL", "MSFT"])

    fav_file: Path = tmp_path / "favorites.json"
    # File must exist
    assert fav_file.exists(), "favorites.json was not created"

    # Check file contents are sorted & deduped
    data = json.loads(fav_file.read_text())
    assert data == ["AAPL", "MSFT"]

    # load_favorites should match
    assert load_favorites() == ["AAPL", "MSFT"]
