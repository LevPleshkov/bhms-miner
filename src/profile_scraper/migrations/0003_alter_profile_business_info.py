# Generated by Django 4.2 on 2023-04-11 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile_scraper', '0002_rename_businsess_info_profile_business_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='business_info',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='profile_scraper.businessinfo', verbose_name='Business Info'),
        ),
    ]
