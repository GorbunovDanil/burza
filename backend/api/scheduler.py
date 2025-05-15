from apscheduler.schedulers.background import BackgroundScheduler
from .pipeline import run
def start():
    sched = BackgroundScheduler(timezone="UTC")
    sched.add_job(run, "cron", hour="0,6,12,18", minute=0)
    sched.start()
