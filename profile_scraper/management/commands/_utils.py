""" When importing profiles or posts, these are commonly used 
    constants and functions.
"""
from os.path import exists
from lxml import etree
from django.core.management.base import CommandError

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


def _get_root(self, path) -> etree.Element:
    """ Get root element of XML file. """
    if not path or not exists(path):
        raise CommandError(self.style.ERROR("File path does not exist"))
    return etree.parse(path).getroot()
