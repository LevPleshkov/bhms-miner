from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandError, CommandParser

from profile_scraper.models import Post, Hashtag, Location


class Command(BaseCommand):
    help = 'Upload existing posts from xml file'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('-l', '--load', type=str,
                            help='Specify path to xml-file to load posts from',)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        from django.utils import timezone
        from os.path import exists
        from pandas import read_xml, to_datetime

        load_path = options['load']

        if load_path:
            if not exists(load_path):
                raise CommandError('File path does not exist')

            from ._post_columns import post_columns
            posts = read_xml(load_path)
            posts = posts[post_columns]
            posts = posts.reset_index()
            posts['timestamp'] = to_datetime(posts['timestamp'])

            # insert all unique hashtags
            from lxml import etree
            tree_root = etree.parse(load_path).getroot()
            hashtags = set()
            for node in tree_root:
                hashtags.update(
                    [hashtag.text for hashtag in node.findall('hashtags') if hashtag.text is not None])
            hashtag_objs = [Hashtag(title=hashtag, created=timezone.now(), modified=timezone.now())
                            for hashtag in hashtags]
            Hashtag.objects.bulk_create(hashtag_objs, ignore_conflicts=True)

            # insert all unique locations
            for _, post in posts[['locationName', 'locationId']].dropna().iterrows():
                eid = int(post['locationId'])
                name = post['locationName']
                Location.objects.get_or_create(
                    external_id=eid,
                    name=name,
                )

            # insert posts
            # for post in posts.iterrows():
            #     Post.objects.get_or_create(
            #         owner_username = post['ownerUsername'],
            #         likes_count = post['likesCount'],
            #         caption = post['caption'],
            #         comments_count = post['commentsCount'],
            #         timestamp = post['timestamp'],
            #         owner_username = post['locationName'],
            #         is_sponseored = post['isSponsored'],
            #     )

            # self.stdout.write(col)
