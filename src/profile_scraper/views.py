from django.db.models import Sum
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from .models import Hashtag, Location, Post, Profile


def index(request):
    template = loader.get_template('profile_scraper/index.html')
    context = {
        'scraper_is_active': False,
        'profiles_count': Profile.objects.count(),
        'top_profiles_count': Profile.objects.filter(
            followers__gte=400_000).count(),
        'profiles_scraped_count': Profile.objects.filter(
            followers__isnull=False).count(),
        'posts_count': Post.objects.count(),
        'posts_scraped_count': Post.objects.aggregate(
            Sum('scrape_count', default=0))['scrape_count__sum'],
        'hashtags_count': Hashtag.objects.count(),
        'hashtags_scraped_count': Hashtag.objects.aggregate(
            Sum('scrape_count', default=0))['scrape_count__sum'],
        'locations_count': Location.objects.count(),
        'locations_scraped_count': Location.objects.aggregate(
            Sum('scrape_count', default=0))['scrape_count__sum'], }
    return HttpResponse(template.render(context, request))
