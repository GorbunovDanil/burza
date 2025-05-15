from tiingo import TiingoClient
from types import SimpleNamespace
import pandas as pd
import datetime as dt

# Start with a placeholder so tests can monkey-patch .client.get_dataframe
client: object = SimpleNamespace()

def _ensure_client() -> TiingoClient:
    """
    Lazily initialize and return the TiingoClient singleton,
    but if our placeholder already has get_dataframe (e.g. test),
    do NOT overwrite it.
    """
    global client
    if not hasattr(client, "get_dataframe"):
        from django.conf import settings
        client = TiingoClient({
            "session": {"timeout": 10},
            "api_key": settings.TIINGO_TOKEN,
        })
    return client

def last_n_days(ticker: str, n: int = 5) -> pd.Series:
    """
    Fetch the last `n` trading days of adjusted-close prices for `ticker`.
    Returns a pandas Series indexed by date.
    """
    end   = dt.date.today()
    start = end - dt.timedelta(days=n + 1)
    df = _ensure_client().get_dataframe(
        ticker,
        metric_name="adjClose",
        startDate=start.isoformat(),
        endDate=end.isoformat(),
        frequency="daily",
    )
    return df["adjClose"]
