# Generated by Django 4.2 on 2023-04-12 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile_scraper', '0006_location_is_authentic_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='external_id',
            field=models.CharField(max_length=60, null=True, unique=True, verbose_name='External ID'),
        ),
        migrations.AlterField(
            model_name='location',
            name='external_id',
            field=models.CharField(max_length=60, null=True, unique=True, verbose_name='External ID'),
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=300, verbose_name='Location Name'),
        ),
        migrations.AlterField(
            model_name='location',
            name='slug',
            field=models.SlugField(max_length=300, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='post',
            name='comments_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='Comments Count'),
        ),
        migrations.AlterField(
            model_name='post',
            name='external_id',
            field=models.CharField(max_length=60, null=True, unique=True, verbose_name='External ID'),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='Likes Count'),
        ),
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Timestamp'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='external_id',
            field=models.CharField(max_length=60, null=True, unique=True, verbose_name='External ID'),
        ),
    ]
