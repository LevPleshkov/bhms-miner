import json
from decouple import config
from typing import Union
from urllib.request import ProxyHandler, build_opener

from urllib.error import HTTPError, URLError
from http.client import IncompleteRead, RemoteDisconnected
from requests.exceptions import SSLError as requestsSSLError
from ssl import SSLError as sslSSLError
from json import JSONDecodeError

from django.db.models import F

from profile_scraper.models import Post, Profile, BusinessInfo


GET_PROFILE_URL = 'https://www.instagram.com/{{ username }}/?__a=1&__d=dis'
COUNTRY_CODE = 'au'

TARGET_FOLLOWERS_COUNT = 5e5
TARGET_TOLERANCE = 1e5

opener = build_opener(ProxyHandler({
    'http': f"customer-{config('OXILAB_USER')}-cc-{COUNTRY_CODE}:{config('OXILAB_PASSWORD')}@pr.oxylabs.io:7777",
    'https': f"customer-{config('OXILAB_USER')}-cc-{COUNTRY_CODE}:{config('OXILAB_PASSWORD')}@pr.oxylabs.io:7777", }))


def config(country_code: str) -> None:
    """ Set configuration.
    """
    global COUNTRY_CODE
    COUNTRY_CODE = country_code if country_code else COUNTRY_CODE


def get_all_usernames_to_scrape(cutoff: int = 0) -> set[str]:
    """ Finds owners of posts that have not yet been scraped 
        ordered by descending priority (by likes count) and have 
        more than the specified amount of likes.
    """
    #  TODO: add usernames of empty profiles, too
    owners = Post.objects \
        .filter(likes_count__gt=cutoff) \
        .order_by('-likes_count') \
        .values_list('owner_username', flat=True)
    usernames = Profile.objects \
        .filter(followers__isnull=False) \
        .values_list('username', flat=True)
    return set([username for username in list(owners)
                if username not in list(usernames)])


def get_hidden_usernames_to_scrape() -> set[str]:
    """ Finds owners of posts with likes count hidden. """
    owners = Post.objects \
        .filter(likes_count=-1) \
        .values_list('owner_username', flat=True)
    return set(owners)


def get_top_usernames_to_scrape(followers_target: int = TARGET_FOLLOWERS_COUNT,
                                tolerance: int = TARGET_TOLERANCE) -> set[str]:
    """ Finds usernames that need to be rescraped and are close 
        to the specified followers count within a specified tolerance, 
        i.e. if target is 500k and tolarance is 100k, it will return 
        all those with followers in range of 400–500k.
    """
    usernames = Profile.objects \
        .filter(followers__lte=followers_target,
                followers__gte=(followers_target-tolerance)) \
        .values_list('username', flat=True)
    return set(usernames)


def fetch_profile_data(username: str) -> dict[str, Union[str, int, bool]]:
    """ Performs HTTP request to Instagram get profile data. 
    """
    url = GET_PROFILE_URL.replace('{{ username }}', username)
    try:
        response = opener.open(url).read()
        if response:
            profile_json = json.loads(response)
            return _parse_profile(profile_json)
    except HTTPError:
        return {'username': username, 'error': 'unauthorized'}
    except URLError:
        return {'username': username, 'error': 'bad gateway'}
    except IncompleteRead:
        return {'username': username, 'error': 'incomplete read'}
    except RemoteDisconnected:
        return {'username': username, 'error': 'disconnected'}
    except (requestsSSLError, sslSSLError):
        return {'username': username, 'error': 'ssl error'}
    except KeyError:
        return {'username': username, 'error': 'key error'}
    except JSONDecodeError:
        return {'username': username, 'error': 'json decoder error'}
    except TimeoutError:
        return {'username': username, 'error': 'timeout error'}


def update_profiles_data(profiles: list[dict[str, Union[str, int, bool]]]):
    """ Updates profiles with new data. 
    """
    for profile in profiles:
        binfo_obj, _ = BusinessInfo.objects.get_or_create(
            category=profile['Business category'],
            contact_method=profile['Business contact method'],
            address=profile['Business address'],
            email=profile['Business e-mail'],
            phone=profile['Business phone number'],)
        profile_obj, created = Profile.objects.update_or_create(
            external_id=profile['ID'],
            defaults={'username': profile['Username'],
                      'full_name': profile['Full name'],
                      'biography': profile['Biography'],
                      'followers': profile['Followers'],
                      'followees': profile['Followees'],
                      'category': profile['Category'],
                      'profile_pic': profile['Profile pic'],
                      'is_business': profile['Is business'],
                      'business_info': binfo_obj, },)
        if not created:
            profile_obj.scrape_count = F('scrape_count') + 1
            profile_obj.save()


def _parse_profile(profile_json) -> dict[str, Union[str, int, bool]]:
    """ Returns flat dictionary. 
    """
    return {
        'ID': profile_json['graphql']['user']['id'],
        'Full name': profile_json['graphql']['user']['full_name'],
        'Username': profile_json['graphql']['user']['username'],
        'Biography': profile_json['graphql']['user']['biography'],
        'Followers': profile_json['graphql']['user']['edge_followed_by'][
            'count'
        ],
        'Followees': profile_json['graphql']['user']['edge_follow']['count'],
        'Category': profile_json['graphql']['user']['category_name'],
        'Profile pic': profile_json['graphql']['user']['profile_pic_url'],
        'Is business': profile_json['graphql']['user']['is_business_account'],
        'Business address': profile_json['graphql']['user'][
            'business_address_json'
        ],
        'Business e-mail': profile_json['graphql']['user']['business_email'],
        'Business phone number': profile_json['graphql']['user'][
            'business_phone_number'
        ],
        'Business category': profile_json['graphql']['user'][
            'business_category_name'
        ],
        'Business contact method': profile_json['graphql']['user'][
            'business_contact_method'
        ],
    }
