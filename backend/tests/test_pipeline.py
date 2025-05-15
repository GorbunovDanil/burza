import pandas as pd
from api.pipeline import run
from api.files import save_favorites

def test_pipeline_filters_and_post(monkeypatch):
    """
    • “BAD” must be filtered out (always falling)
    • “GOOD” must pass (rising)
    • The HTTP POST payload therefore contains only GOOD
    """
    save_favorites(["BAD", "GOOD"])

    #  --- Patch helpers inside api.pipeline -------------------------------
    def fake_series(ticker, *_):
        return pd.Series([3, 2, 1]) if ticker == "BAD" else pd.Series([1, 2, 3])

    monkeypatch.setattr("api.pipeline.load_favorites", lambda: ["BAD", "GOOD"])
    monkeypatch.setattr("api.pipeline.last_n_days", fake_series, raising=True)

    posted = {}

    class DummyClient:
        def __init__(self, **kwargs):
            pass
        def post(self, url, json, **kwargs):
            posted["url"], posted["json"] = url, json
            class R: status_code = 200
            return R()
        def __enter__(self): return self
        def __exit__(self, *a): pass

    monkeypatch.setattr("api.pipeline.httpx.Client", DummyClient, raising=True)
    # ----------------------------------------------------------------------

    run()

    assert posted["url"].endswith("/liststock")
    assert {item["name"] for item in posted["json"]} == {"GOOD"}
