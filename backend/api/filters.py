import pandas as pd

def last_three_days_falling(series: pd.Series) -> bool:
    """True if price fell on each of the **last 3** trading days."""
    diffs = series.tail(3).diff().dropna()   # [-1, -1] for 3→2→1
    return bool((diffs < 0).all())

def two_falls_in_five(series: pd.Series) -> bool:
    """True if price fell **more than twice** in the last 5 days."""
    falls = (series.tail(5).diff().fillna(0) < 0).sum()
    return bool(falls > 2)
