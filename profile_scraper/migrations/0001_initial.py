# Generated by Django 4.2 on 2023-04-03 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100, verbose_name='Business Category')),
                ('contact_method', models.CharField(max_length=15, verbose_name='Contact Method')),
                ('address', models.CharField(max_length=60, verbose_name='Address')),
                ('email', models.EmailField(max_length=30, verbose_name='Email')),
                ('phone', models.CharField(max_length=15, verbose_name='Phone')),
            ],
            options={
                'verbose_name': 'Business Category',
                'verbose_name_plural': 'Business Categories',
                'ordering': ('category',),
            },
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Hashtag')),
            ],
            options={
                'verbose_name': 'Hashtag',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(max_length=60, verbose_name='External ID')),
                ('name', models.CharField(max_length=300, verbose_name='Location Name')),
            ],
            options={
                'verbose_name': 'Location',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(max_length=60, verbose_name='External ID')),
                ('full_name', models.CharField(max_length=60, verbose_name='Full Name')),
                ('username', models.CharField(max_length=60, verbose_name='Username')),
                ('biography', models.CharField(max_length=300, verbose_name='Biography')),
                ('followers', models.IntegerField(verbose_name='Followed By')),
                ('followees', models.IntegerField(verbose_name='Follows')),
                ('category', models.CharField(max_length=100, verbose_name='Profile Category')),
                ('profile_pic', models.URLField(verbose_name='Profile Picture')),
                ('is_business', models.BooleanField(default=False, verbose_name='Is Business')),
                ('businsess_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='profile_scraper.businessinfo')),
            ],
            options={
                'verbose_name': 'Profile',
                'ordering': ('username',),
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_username', models.CharField(max_length=60, verbose_name="Owner's Username")),
                ('likes_count', models.IntegerField(verbose_name='Likes Count')),
                ('comments_count', models.IntegerField(verbose_name='Comments Count')),
                ('caption', models.TextField(verbose_name='Caption')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp')),
                ('is_sponseored', models.BooleanField(verbose_name='Is Sponsored')),
                ('hashtags', models.ManyToManyField(to='profile_scraper.hashtag')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profile_scraper.location')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='profile_scraper.profile')),
            ],
            options={
                'verbose_name': 'Post',
                'ordering': ('likes_count', 'owner_username'),
            },
        ),
    ]
