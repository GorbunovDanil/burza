import pandas as pd

from api.filters import last_three_days_falling, two_falls_in_five

def make_series(*vals):
    return pd.Series(vals)

def test_last_three_days_falling_true():
    # strictly decreasing
    s = make_series(10, 9, 8, 7, 6)
    assert last_three_days_falling(s) is True

def test_last_three_days_falling_false():
    # one up-tick breaks it
    s = make_series(10, 9, 8, 9, 6)
    assert last_three_days_falling(s) is False

def test_two_falls_in_five_true():
    # three falls in last five
    s = make_series(5, 4, 5, 4, 3, 2)
    assert two_falls_in_five(s) is True

def test_two_falls_in_five_false():
    # only one or two falls
    s = make_series(1, 2, 1, 2, 1, 2)
    assert two_falls_in_five(s) is False
