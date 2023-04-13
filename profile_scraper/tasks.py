from time import sleep
from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task()
def get_profile_task():
    sleep(10)
    logger.info('The sample task just ran.')
