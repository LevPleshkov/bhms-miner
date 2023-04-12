from django.db import models
from .meta import ScrapeInfo


class BusinessInfo(models.Model):
    category = models.CharField(
        'Business Category', max_length=100, null=True, blank=True)
    contact_method = models.CharField(
        'Contact Method', max_length=50, default='UNKNOWN')
    address = models.CharField(
        'Address', max_length=100, null=True, blank=True)
    email = models.EmailField('Email', max_length=100, null=True, blank=True)
    phone = models.CharField('Phone', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Business Info'
        ordering = ('category',)

    def __str__(self) -> str:
        return f'{self.category}'


class Profile(ScrapeInfo):
    full_name = models.CharField(
        'Full Name', max_length=100, null=True, blank=True)
    username = models.CharField('Username', max_length=100, unique=True)
    biography = models.CharField(
        'Biography', max_length=1_000, null=True, blank=True)
    followers = models.IntegerField('Followed By', null=True, blank=True)
    followees = models.IntegerField('Follows', null=True, blank=True)
    category = models.CharField(
        'Profile Category', max_length=100, null=True, blank=True)
    profile_pic = models.URLField(
        'Profile Picture', max_length=1_000, null=True, blank=True)
    is_business = models.BooleanField('Is Business', default=False)
    business_info = models.ForeignKey(
        BusinessInfo, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        verbose_name = 'Profile'
        ordering = ('username',)

    def __str__(self) -> str:
        return f'{self.username}'
