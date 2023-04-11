from django.db import models
from .meta import ScrapeInfo


class BusinessInfo(models.Model):
    category = models.CharField(
        'Business Category', max_length=100, blank=True)
    contact_method = models.CharField('Contact Method', max_length=15)
    address = models.CharField('Address', max_length=60, null=True, blank=True)
    email = models.EmailField('Email', max_length=30, null=True, blank=True)
    phone = models.CharField('Phone', max_length=15, null=True, blank=True)

    class Meta:
        verbose_name = 'Business Info'
        verbose_name_plural = 'Business Infos'
        ordering = ('category',)

    def __str__(self) -> str:
        return f'{self.category}'


class Profile(ScrapeInfo):
    full_name = models.CharField('Full Name', max_length=60)
    username = models.CharField('Username', max_length=60, unique=True)
    biography = models.CharField('Biography', max_length=300, null=True, blank=True)
    followers = models.IntegerField('Followed By', null=True, blank=True)
    followees = models.IntegerField('Follows', null=True, blank=True)
    category = models.CharField('Profile Category', max_length=100, null=True, blank=True)
    profile_pic = models.URLField('Profile Picture', null=True, blank=True)
    is_business = models.BooleanField('Is Business', default=False)

    businsess_info = models.OneToOneField(
        BusinessInfo, on_delete=models.CASCADE, verbose_name='Business Info'
    )

    class Meta:
        verbose_name = 'Profile'
        ordering = ('username',)

    def __str__(self) -> str:
        return f'{self.username}'
