from django.db import models
from .profile import Profile


class Hashtag(models.Model):
    title = models.CharField('Hashtag', max_length=100)

    class Meta:
        verbose_name = 'Hashtag'

    def __str__(self) -> str:
        return f'{self.title}'


class Location(models.Model):
    external_id = models.CharField('External ID', max_length=60)
    name = models.CharField('Location Name', max_length=300)

    class Meta:
        verbose_name = 'Location'

        def __str__(self) -> str:
            return f'{self.name}'


class Post(models.Model):
    owner_username = models.CharField('Owner\'s Username', max_length=60)
    likes_count = models.IntegerField('Likes Count')
    comments_count = models.IntegerField('Comments Count')
    caption = models.TextField('Caption')
    timestamp = models.DateTimeField('Timestamp')
    is_sponseored = models.BooleanField('Is Sponsored')
    hashtags = models.ManyToManyField(Hashtag)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    profile = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Post'
        ordering = ('likes_count', 'owner_username',)

    def __str__(self) -> str:
        return f'{self.owner_username}: {self.caption[:10]}'
