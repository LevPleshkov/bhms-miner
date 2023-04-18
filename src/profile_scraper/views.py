from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from .models import Hashtag, Location, Post, Profile


def index(request):
    template = loader.get_template('profile_scraper/index.html')
    profiles_cnt = Profile.objects.count()
    posts_cnt = Post.objects.count()
    hashtags_cnt = Hashtag.objects.count()
    locations_cnt = Location.objects.count()
    context = {
        'profiles_count': profiles_cnt,
        'posts_count': posts_cnt,
        'hashtags_count': hashtags_cnt,
        'locations_count': locations_cnt,
    }
    return HttpResponse(template.render(context, request))
