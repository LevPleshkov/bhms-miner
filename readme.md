# BHMS Miner

## Requirements

All the production requirements are included in **requirements.txt** file, wherease development requirements are added to them in **requirements.dev.txt** file.  To activate virtual environment in */venv* folder:
```bash
python -m venv venv
```
Install development requirements:
```bash
pip install -r src/requirements.dev.txt
```


## Run Server Locally Without Docker

*The following commands are executed from **src/** folder.*

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


To revoke ALL the tasks form Celery use:
```bash
celery -A bhms_miner purge
```


## Deployment

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```
```bash
docker-compose -f docker-compose.prod.yml down -v
```


## TODO

### List

- [x] model database
- [x] create a homescreen dashboard
- [x] add meta (created, updated, scraped) info to models
- [x] upload existing posts from xml-files to database
- [x] upload existing profiles from csv-files to database
- [x] add scraping mechanism for profiles
- [x] dockerize

@@@ MVP Milestone @@@

- [ ] authentication
- [ ] upload posts and profiles from gui
- [ ] add favicon
- [ ] add `used_count` field to hashtag entity
- [ ] download posts and profiles, hashtags and location from database
- [ ] ? split tasks in queues
- [ ] add mechanism to set scraping parameters, start and stop scraping
- [ ] periodically remove unpopular hashtags from database
- [ ] add scraping mechanism for posts

### Approach to implement

Profiles do not have location info, while posts have location info and hashtags.  That's why we first scrape posts by locations and hashtags, then select the most promising of the to scrape profiles ny their authors.  There are posts with hidden likes (-1) that seem to be the most fruitful by how many profiles with high amounts of followers they allow to scrape.  There are posts that have just been published and their small likes count doesn't mean they were published by unpopular authors.  The following scheme seems to be optimal:

- Scrape all posts with hidden likes,
- Scrape all posts with likes count more than 10 (posts with lesser values do not result many popular profiles for the cost of residence proxies),
- Periodically rescrape profiles that are close to targeted amount of followers.
