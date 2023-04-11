from django.db import models
from .profile import Profile
from .meta import ScrapeInfo


class Hashtag(ScrapeInfo):
    title = models.CharField('Hashtag', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Hashtag'

    def __str__(self) -> str:
        return f'{self.title}'


class Location(ScrapeInfo):
    name = models.CharField('Location Name', max_length=300, unique=True)
    slug = models.SlugField('Slug', max_length=300, unique=True)

    class Meta:
        verbose_name = 'Location'

        def __str__(self) -> str:
            return f'{self.name}'


class Post(ScrapeInfo):
    owner_username = models.CharField('Owner\'s Username', max_length=60)
    likes_count = models.IntegerField('Likes Count')
    comments_count = models.IntegerField('Comments Count')
    caption = models.TextField('Caption', null=True, blank=True)
    timestamp = models.DateTimeField('Timestamp')
    is_sponsored = models.BooleanField('Is Sponsored', default=False)
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    location = models.ForeignKey(
        Location, on_delete=models.DO_NOTHING, null=True, blank=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        verbose_name = 'Post'
        ordering = ('likes_count', 'owner_username',)

    def __str__(self) -> str:
        return f'{self.owner_username}: {self.caption[:10]}'
