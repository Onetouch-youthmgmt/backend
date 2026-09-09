import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database.database import supabase

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()

def ping_supabase():
    """Touches the Supabase DB so the free-tier project doesn't auto-pause from inactivity."""
    try:
        supabase.table("sabha_centers").select("id").limit(1).execute()
        logger.info("Supabase keep-alive ping succeeded")
    except Exception as e:
        logger.error("Supabase keep-alive ping failed: %s", str(e))

def start_scheduler():
    scheduler.add_job(ping_supabase, CronTrigger(hour=3, minute=0), id="supabase_keep_alive")
    scheduler.start()

def stop_scheduler():
    scheduler.shutdown(wait=False)
