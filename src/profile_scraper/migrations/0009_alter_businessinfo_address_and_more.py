# Generated by Django 4.2 on 2023-04-12 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_scraper', '0008_alter_location_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessinfo',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='businessinfo',
            name='contact_method',
            field=models.CharField(max_length=50, verbose_name='Contact Method'),
        ),
        migrations.AlterField(
            model_name='businessinfo',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='businessinfo',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='hashtag',
            name='title',
            field=models.CharField(max_length=2200, unique=True, verbose_name='Hashtag'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=500, verbose_name='Location Name'),
        ),
        migrations.AlterField(
            model_name='location',
            name='slug',
            field=models.SlugField(blank=True, max_length=500, null=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.TextField(blank=True, max_length=2200, null=True, verbose_name='Caption'),
        ),
        migrations.AlterField(
            model_name='post',
            name='owner_username',
            field=models.CharField(max_length=100, verbose_name="Owner's Username"),
        ),
        migrations.AlterField(
            model_name='profile',
            name='biography',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Biography'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='full_name',
            field=models.CharField(max_length=100, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=100, unique=True, verbose_name='Username'),
        ),
    ]
