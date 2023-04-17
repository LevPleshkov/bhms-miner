from time import sleep
from typing import Sequence
from numpy.random import uniform

from celery import shared_task
from celery.canvas import group, chord, chunks
from celery.utils.log import get_task_logger

from profile_scraper.service import profile


logger = get_task_logger(__name__)


@shared_task
def scrape_all_profiles():
    """ Scrape by all usernames have not yet been scraped.
    """
    scrape_profiles.s(profile.get_all_usernames_to_scrape(cutoff=10))()


@shared_task
def scrape_top_profiles():
    """ Scrape by usernames of the most promising profiles.
    """
    scrape_profiles.s(profile.get_top_usernames_to_scrape())()


@shared_task
def scrape_hidden_profiles():
    """ Scrape by usernames of owners of posts with hidden
        likes count.
    """
    scrape_profiles.s(profile.get_hidden_usernames_to_scrape())()


@shared_task
def scrape_profiles(usernames: list[str]):
    """ Gradually scrape profiles by given usernames.
    """
    # TODO: propably, there is another more Celery-compliant solution,
    # it is not recommended to run subtasks syncronously in a task.
    if not isinstance(usernames, list) and not isinstance(usernames, tuple):
        usernames = list(usernames)

    def batches(seq: Sequence, size: int = 7):
        for i in range(0, len(seq), size):
            yield seq[i:i + size]

    for batch in batches(usernames):
        scrape_tasks = group([scrape_profile.s(username).set(countdown=uniform(0, 7))
                              for username in batch])
        scrape_n_save = chord(scrape_tasks)(save_profiles.s())
        scrape_n_save.get(disable_sync_subtasks=False)


@shared_task
def scrape_profile(username: str):
    """ Scrape a single profile by username.
    """
    return profile.fetch_profile_data(username)


@shared_task
def save_profiles(results: list[dict]):
    """ Save scraped profiles to database.
    """
    profiles = [result for result in results if 'error' not in result.keys()]
    profile.update_profiles_data(profiles)
