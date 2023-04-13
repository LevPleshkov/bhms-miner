# Requirements
All the production requirements are included in **requirements.txt** file, wherease development requirements are added to them in **requirements_dev.txt** file.

# Run Server
This project uses Django and Celery.  To have Celery auto-reloaded when changes to **.py** files happen during development, start the server with the following commands:

1. In the first terminal, start **Django**:
```bash
python manage.py runserver
```
2. In the second terminal, start **Celery worker** (without it, scheduled tasks won't be executed):
```bash
watchfiles --filter python 'celery -A bhms_miner worker -l info'
```
3. In the third terminal, start **Celery beat**:
```bash
watchfiles --filter python 'celery -A bhms_miner beat -l info'
```
Feel free to change log levels and pass optional arguments.


# TODO List
- [x] add meta (created, updated, scraped) info to models
- [x] upload existing posts from xml-files to database
- [x] upload existing profiles from csv-files to database
- [ ] add scraping mechanism for profiles
- [ ] add `used_count` field to hashtag entity
- [ ] download posts and profiles, hashtags and location from database
- [ ] periodically remove unpopular hashtags from database
- [ ] add scraping mechanism for posts
