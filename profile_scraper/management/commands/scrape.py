from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandParser, CommandError

from profile_scraper.tasks import (
    scrape_all_profiles, scrape_top_profiles, scrape_hidden_profiles, scrape_profiles)
from profile_scraper.service import profile
from bhms_miner import celery


class Command(BaseCommand):
    help = ""

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('action', type=str, choices=['run', 'stop'],
                            help="Run or stop the task.  When stopping the task, \
                                specify the id")
        parser.add_argument('-m', '--mode', type=str, choices=['all', 'top', 'hidden'],
                            help="What usernames to scrape: all, top (close to the target \
                                amount of followers), or hidden (owners of posts with \
                                hidden likes count)")
        parser.add_argument('-c', '--country-code', type=str,
                            help="Country code in two-letter format, \
                            example - 'au' for Australia")
        parser.add_argument('-t', '--task_id', type=str,
                            help="Id of the task that has to be revoked")

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        action = options['action']
        if action == 'run':
            profile.config(country_code=options['country_code'])
            # task_id = scrape_profiles.delay(['balitecture', 'balilivin',
            #                                  'jawapos', 'lux_arcadiaz',
            #                                  'nameatswell', 'balikoitour',
            #                                  'ahsyaf.rlh', 'firputra27',
            #                                  'iisrun', 'im_anshumaan',
            #                                  'alexsantoso52'])
            if options['mode'] == 'top':
                task_id = scrape_top_profiles.delay()
            elif options['mode'] == 'hidden':
                task_id = scrape_hidden_profiles.delay()
            else:
                task_id = scrape_all_profiles.delay()
            self.stdout.write(self.style.SUCCESS(
                f'Task with id {task_id} has just started!'))
        elif action == 'stop':
            if options['task_id'] == 'all':
                celery.app.control.revoke(self.running_tasks, terminate=True)
            else:
                celery.app.control.revoke(options['task_id'], terminate=True)
