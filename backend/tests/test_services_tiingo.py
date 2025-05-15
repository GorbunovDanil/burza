import datetime as dt
import pandas as pd
import respx

from api.services.tiingo import last_n_days, client

@respx.mock
def test_last_n_days(monkeypatch):
    today = dt.date.today()
    dates = [today - dt.timedelta(days=i) for i in range(3)]
    values = [100, 101, 102]
    fake_df = pd.DataFrame({"adjClose": values}, index=dates)

    # Patch client.get_dataframe even if it doesn't exist yet
    monkeypatch.setattr(
        client, "get_dataframe",
        lambda *args, **kwargs: fake_df,
        raising=False
    )

    series = last_n_days("MSFT", n=2)
    # Must return a pd.Series of our values
    assert isinstance(series, pd.Series)
    assert list(series) == values
