from .files import load_favorites
from .services.tiingo import last_n_days
from .filters import last_three_days_falling, two_falls_in_five
from django.conf import settings
import httpx, logging, time

log = logging.getLogger("burza")

def run():
    kept = []
    for ticker in load_favorites():
        s = last_n_days(ticker, 5)
        if last_three_days_falling(s):              # filter a)
            log.info("%s dropped 3 straight – out", ticker); continue
        if two_falls_in_five(s):                    # filter b)
            log.info("%s fell >2× in 5 days – out", ticker); continue
        kept.append(ticker)

    if not kept:
        log.info("Nothing left after filters"); return

    payload = [{"name": t, "date": int(time.time()), "rating": 0, "sale": 0}
               for t in kept]

    with httpx.Client(verify="certs/partner_ca.pem") as c:
        r = c.post("https://partner-url:8000/liststock", json=payload, timeout=10)
        log.info("Sent %s tickers, partner→%s", len(payload), r.status_code)
