import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from database.database import supabase

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

def ping_supabase():
    """Inserts a row into cron_test_log so the free-tier Supabase project
    doesn't auto-pause from inactivity. Uses a POST (insert) instead of a
    GET (select) so each run leaves a visible, checkable row."""
    try:
        supabase.table("cron_test_log").insert({"message": "test"}).execute()
        logger.info("Supabase keep-alive ping succeeded")
    except Exception as e:
        logger.error("Supabase keep-alive ping failed: %s", str(e))

def start_scheduler():
    scheduler.add_job(ping_supabase, IntervalTrigger(days=2), id="supabase_keep_alive")
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown(wait=False)
