from backend.api.files import load_favorites, save_favorites
def test_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr("backend.api.files.DATA", tmp_path)
    save_favorites(["MSFT", "AAPL"])
    assert load_favorites() == ["AAPL", "MSFT"]
