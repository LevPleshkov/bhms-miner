# Generated by Django 4.2 on 2023-04-05 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile_scraper', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='businessinfo',
            options={'ordering': ('category',), 'verbose_name': 'Business Info', 'verbose_name_plural': 'Business Infos'},
        ),
        migrations.AlterField(
            model_name='businessinfo',
            name='address',
            field=models.CharField(blank=True, max_length=60, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='businessinfo',
            name='category',
            field=models.CharField(blank=True, max_length=100, verbose_name='Business Category'),
        ),
        migrations.AlterField(
            model_name='businessinfo',
            name='email',
            field=models.EmailField(blank=True, max_length=30, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='businessinfo',
            name='phone',
            field=models.CharField(blank=True, max_length=15, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='post',
            name='hashtags',
            field=models.ManyToManyField(null=True, to='profile_scraper.hashtag'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='businsess_info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='profile_scraper.businessinfo', verbose_name='Business Info'),
        ),
    ]
