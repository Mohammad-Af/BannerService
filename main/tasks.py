from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
import os

from BannerService.settings import BASE_DIR

logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute=0, hour='*/12')), name="data_loader", ignore_result=True)
def start():
    logger.info("Getting new data from S3")
    os.system(f"source {os.path.join(BASE_DIR, 'main/celery_task.sh')}")
    logger.info("Done")
