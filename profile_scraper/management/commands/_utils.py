""" When importing profiles or posts, these are commonly used 
    constants and functions.
"""
from os.path import exists
from typing import Optional
from lxml import etree
from django.core.management.base import BaseCommand, CommandError

# Tags in xml-file that contain required information about post
post_tags = ['id', 'caption', 'hashtags', 'timestamp',
             'commentsCount', 'likesCount', 'isSponsored',
             'locationId', 'locationName', 'ownerUsername', 'ownerId',]

# Tag that contain city location info
city_info_tag = 'city_info'
# Tag that contain other locations info
location_list_tag = 'location_list'
# Tags in xml-file that contain required information about location
location_tags = ['id', 'name', 'slug']


def _get_root(cmd: BaseCommand, path: str) -> Optional[etree.Element]:
    """ Get root element of XML file. """
    if _validate_path(cmd, path):
        return etree.parse(path).getroot()


def _validate_path(cmd: BaseCommand, path: str) -> bool:
    if not path or not exists(path):
        cmd.stdout.write(f'here')
        raise CommandError(cmd.style.ERROR("File path does not exist"))
    return True
