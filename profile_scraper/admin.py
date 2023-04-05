from django.contrib import admin

from .models import (
    Hashtag, Location, Post,
    BusinessInfo, Profile,
)

admin.site.register(Hashtag)
admin.site.register(Location)
admin.site.register(Post)
admin.site.register(BusinessInfo)
admin.site.register(Profile)
