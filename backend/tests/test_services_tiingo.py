import datetime as dt
import pandas as pd
import respx
from backend.api.services.tiingo import last_n_days

@respx.mock
def test_last_n(monkeypatch):
    today = dt.date.today()
    fake = pd.Series([1, 2, 3],
                     index=[today - dt.timedelta(i) for i in range(3)])

    # Monkey-patch Tiingo client so no real HTTP happens
    monkeypatch.setattr(
        "api.services.tiingo.client.get_dataframe",
        lambda *a, **k: fake.to_frame("adjClose"),
        raising=False, 
    )

    s = last_n_days("MSFT", 2)
    assert len(s) == 3
    assert list(s) == [1, 2, 3]
