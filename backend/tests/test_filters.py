import pandas as pd
from backend.api.filters import last_three_days_falling, two_falls_in_five

def series(*vals):               # helper
    return pd.Series(vals)

def test_3day():
    assert last_three_days_falling(series(5,4,3,2,1)) is True
    assert last_three_days_falling(series(5,4,3,4,1)) is False

def test_2falls():
    assert two_falls_in_five(series(5,4,5,4,3,2)) is True    # 3 falls
    assert two_falls_in_five(series(5,6,5,6,5,6)) is False
