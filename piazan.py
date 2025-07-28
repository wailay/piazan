#!/usr/bin/env -S uv run --script

import datetime
from prayer_times.prayer_times import PrayerTimes
from prayer_times.method import Method
from prayer_times.contants import TIME_FORMAT_12H
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from pydub.playback import _play_with_simpleaudio
from pydub import AudioSegment
import logging
from typing import Dict
from apscheduler.job import Job

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

std_handler = logging.StreamHandler()
std_handler.setFormatter(formatter)

logger = logging.getLogger('piazan')

logger.addHandler(std_handler)
logger.setLevel(logging.INFO)


# holds jobs in memory used for status display
status_jobs: Dict[str, Job] = {}

jobstores = {
    'default': MemoryJobStore(),
}

executors = {
    'default': ThreadPoolExecutor(max_workers=10),
}

job_defaults = {
    'coalesce': True,
    'max_instances': 1,
    'misfire_grace_time': 60,
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

pt_isna = PrayerTimes(method=Method.METHOD_ISNA)
    

LAVAL_LATITUDE = 45.583729
LAVAL_LONGITUDE = -73.750069
LAVAL_TIMEZONE = pytz.timezone("America/Toronto")

Adham_Al_Sharqawe_Adhan_Audio_Segment = AudioSegment.from_mp3("./adhan_sound/Adham-Al-Sharqawe.mp3")

def play_non_blocking(audio_segment):
    playback = _play_with_simpleaudio(audio_segment)
    return playback

def prayer_adhan_function(prayer_name):
    logger.info(f"Playing adhan for {prayer_name}")

    play_non_blocking(Adham_Al_Sharqawe_Adhan_Audio_Segment)


def schedule_prayer_times():
    logger.info("Scheduling prayer times")
    today_date = LAVAL_TIMEZONE.localize(datetime.datetime.now())
    
    logger.info("=== Prayer Times for Montreal, Canada ===")
    logger.info(f"Date: {today_date}")
    logger.info(f"Coordinates: {LAVAL_LATITUDE}, {LAVAL_LONGITUDE}")
    logger.info(f"Method: {pt_isna.get_method()}")

    
    # Get prayer times for today
    times = pt_isna.get_times_for_today(LAVAL_LATITUDE, LAVAL_LONGITUDE, today_date)
    
    # Display prayer times
    prayer_names = {
        'Fajr': 'Fajr',
        'Dhuhr': 'Dhuhr',
        'Asr': 'Asr',
        'Maghrib': 'Maghrib',
        'Isha': 'Isha',
    }
    
    for prayer, time in times.items():
        if prayer in prayer_names:
            hour, minute = time.split(':')
            prayer_datetime = today_date.replace(hour=int(hour), minute=int(minute), second=0)
            logger.info(f"Scheduling {prayer_names[prayer]} for {prayer_datetime} at {time}")
            job = scheduler.add_job(prayer_adhan_function, 'date', run_date=prayer_datetime, args=[prayer_names[prayer]])
            status_jobs[prayer_names[prayer]] = job
    

    
    
def scheduler_status():
    logger.info("========================= Scheduler Status ======================")
    for job_name, job in status_jobs.items():
        logger.info(f"Job {job_name:<30} next run: {job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("========================= Scheduler Status ======================")

if __name__ == "__main__":

    logger.info("Starting scheduler")
    scheduler.start()
    logger.info("Scheduler started")

    schedule_prayer_times()

    # Cron job that runs every midnight and re compute the prayer times
    job = scheduler.add_job(schedule_prayer_times, 'cron', hour=0, minute=0)
    status_jobs['cron_recompute_prayer_times'] = job
    
    logger.info("Piazan is running...")

    scheduler_status()

    while True:
        try:
            pass
        except Exception as e:
            logger.error(f"Error: {e}")
            scheduler.shutdown()
            break


    
    

