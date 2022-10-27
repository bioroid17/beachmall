
from apscheduler.schedulers.background import BackgroundScheduler
from Jobs.jobs import schedule_api
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_api, "cron", hour=0, minute=0)
    # scheduler.add_job(schedule_api, "interval", minutes=1)
    scheduler.start()