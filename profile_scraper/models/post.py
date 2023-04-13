from django.db import models
from django.utils.text import slugify
from .profile import Profile
from .meta import ScrapeInfo

CAPTION_MAX_LENTH = 2_200


class Hashtag(ScrapeInfo):
    title = models.CharField(
        'Hashtag', max_length=CAPTION_MAX_LENTH, unique=True)

    class Meta:
        verbose_name = 'Hashtag'

    def __str__(self) -> str:
        return f'{self.title}'


class Location(ScrapeInfo):
    """ The Location is considered unique by its
         - external_id.
    """
    name = models.CharField('Location Name', max_length=500)
    slug = models.SlugField('Slug', max_length=500, null=True, blank=True)
    is_authentic_slug = models.BooleanField('Is Slug Authentic', default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            self.is_authentic_slug = False
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Location'

        def __str__(self) -> str:
            return f'{self.name}'


class Post(ScrapeInfo):
    """ The Post is considered unique by its
         - external_id,
         - owner_username.
    """
    owner_username = models.CharField('Owner\'s Username', max_length=100)
    likes_count = models.IntegerField('Likes Count', null=True, blank=True)
    comments_count = models.IntegerField(
        'Comments Count', null=True, blank=True)
    caption = models.TextField(
        'Caption', max_length=CAPTION_MAX_LENTH, null=True, blank=True)
    timestamp = models.DateTimeField('Timestamp', null=True, blank=True)
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
