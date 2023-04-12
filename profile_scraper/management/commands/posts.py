from os.path import exists
from lxml import etree
from typing import Any, Optional, List, Dict
from tqdm import tqdm

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.utils import timezone

from profile_scraper.models import (
    Profile, BusinessInfo, Post, Hashtag, Location)


class Command(BaseCommand):
    help = "Download stored in the database or upload existing posts to \
        the database from xml file that was generated by APIFY.\n\n\
        WARNING! If it so happens that some user has altered their username, \
        caption or the likes / comments count of the post with the same Instagram ID \
        these changes will not be updated in the database."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('mode', type=str, choices=['download', 'upload'])
        parser.add_argument('-p', '--path', type=str, required=True,
                           help="Specify path to xml-file with posts that \
                            were scraped by locations or hashtags",)
        parser.add_argument('-b', '--beg', type=int,
                           help="Specify the first item in xml-file \
                            to upload into database, default is 0",)
        parser.add_argument('-e', '--end', type=int,
                           help="Specify the last item in xml-file \
                            to upload into database, default is len(items)",)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        mode = options['mode']
        if mode == 'upload':
            # if load_path := options['path']:
            self._load_posts(options['path'], options['beg'], options['end'])
        else:
            raise CommandError(
                self.style.ERROR('Sorry, only upload functionality is implemented.'),)

    def _load_posts(self, path: str, beg: int = None, end: int = None) -> None:
        root = self._get_root(path)
        posts_cnt = hashtags_cnt = locations_cnt = 0

        # 1. Parse locations fisrt, because we need instagram-generated slugs,
        #   and save the first one because it will not appear in posts.
        locations = self._parse_locations(root)
        if len(locations):
            created = Location.objects.bulk_create(
                [Location(external_id=location['id'],
                          name=location['name'],
                          slug=location['slug'],)
                 for location in locations],
                ignore_conflicts=True,)
            locations_cnt += len(created)

        # 2. Parse posts while saving all objects
        post_tags = ['id', 'caption', 'hashtags', 'timestamp',
                     'commentsCount', 'likesCount', 'isSponsored',
                     'locationId', 'locationName', 'ownerUsername', 'ownerId',]
        items = root.findall('item')
        beg = beg if beg else 0
        end = end if end else len(items)
        for item in tqdm(items[beg:end],
                         ncols=100, unit='item', colour='green'):
            data = [item.xpath(f'{tag}/text()') for tag in post_tags]
            post = dict(zip(post_tags, [part[0] if len(
                part) == 1 else part for part in data]))

            if not self._validate_post_data(post):
                continue

            message = f"Post with ext. id {post['id']} is being updated with:"

            # post
            post_obj, created = Post.objects.get_or_create(
                external_id=post['id'],
                owner_username=post['ownerUsername'],
                defaults={'likes_count': post['likesCount'],
                          'comments_count': post['commentsCount'],
                          'caption': post['caption'],
                          'timestamp': post['timestamp'],
                          'is_sponsored': (post['isSponsored'] == 'true'), },)
            posts_cnt += 1 if created else 0

            # profile
            profile_obj, _ = Profile.objects.get_or_create(
                external_id=post['ownerId'],
                defaults={'username': post['ownerUsername'], },)
            if post_obj.profile_id and post_obj.profile_id != profile_obj.id:
                message += " profile"
            post_obj.profile = profile_obj

            # location
            location = next((location for location in locations
                             if location['id'] == post['locationId']), None,)
            if location:
                location_obj, created = Location.objects.get_or_create(
                    external_id=location['id'],
                    defaults={'name': location['name'],
                              'slug': location['slug'], },)
            else:
                location_obj, created = Location.objects.get_or_create(
                    external_id=post['locationId'],
                    defaults={'name': post['locationName'], })
            locations_cnt += 1 if created else 0
            if post_obj.location_id and post_obj.location_id != location_obj.id:
                message += " location"
            post_obj.location = location_obj

            # hashtags
            created = Hashtag.objects.bulk_create(
                [Hashtag(title=hashtag)
                 for hashtag in post['hashtags']],
                ignore_conflicts=True,)
            hashtag_objs = Hashtag.objects.filter(title__in=post['hashtags'])
            hashtags_cnt += len(created)  # - len(hashtag_objs)
            post_obj.hashtags.add(*hashtag_objs)

            if not message.endswith(':'):
                self.stdout.write(self.style.WARNING(message + "!"))

            post_obj.save()

        self.stdout.write(self.style.SUCCESS(f"Inserted " +
                                             f"{posts_cnt} posts."),)

    def _parse_locations(self, root) -> List[Dict]:
        city_info_tag = 'city_info'
        location_list_tag = 'location_list'
        location_tags = ['id', 'name', 'slug']
        data = [
            *zip(*[root.xpath(f'//item/{city_info_tag}/{tag}/text()')
                   for tag in location_tags]),
            *[tuple([element.text for element in row])
              for row in zip(*[root.xpath(f'//item/{location_list_tag}/{tag}')
                               for tag in location_tags])],]
        return [dict(zip(location_tags, part)) for part in data if part]

    def _get_root(self, path) -> etree.Element:
        if not path or not exists(path):
            raise CommandError(self.style.ERROR("File path does not exist"))
        return etree.parse(path).getroot()

    def _validate_post_data(self, post: dict) -> bool:
        return all([post['id'],
                    post['ownerUsername'], post['timestamp'],
                    post['commentsCount'], post['likesCount']])
