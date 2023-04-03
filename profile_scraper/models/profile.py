from django.db import models


class BusinessInfo(models.Model):
    category = models.CharField('Business Category', max_length=100)
    contact_method = models.CharField('Contact Method', max_length=15)
    address = models.CharField('Address', max_length=60)
    email = models.EmailField('Email', max_length=30)
    phone = models.CharField('Phone', max_length=15)

    class Meta:
        verbose_name = 'Business Category'
        verbose_name_plural = 'Business Categories'
        ordering = ('category',)

    def __str__(self) -> str:
        return f'{self.category}'


class Profile(models.Model):
    external_id = models.CharField('External ID', max_length=60)
    full_name = models.CharField('Full Name', 'full_name', max_length=60)
    username = models.CharField('Username', 'username', max_length=60)
    biography = models.CharField('Biography', 'biography', max_length=300)
    followers = models.IntegerField('Followed By')
    followees = models.IntegerField('Follows')
    category = models.CharField('Profile Category', max_length=100)
    profile_pic = models.URLField('Profile Picture')
    is_business = models.BooleanField('Is Business', default=False)

    businsess_info = models.OneToOneField(
        BusinessInfo, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Profile'
        ordering = ('username',)

    def __str__(self) -> str:
        return f'{self.username}'
