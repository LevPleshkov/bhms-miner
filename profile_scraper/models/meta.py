from django.db import models
from django.utils import timezone


class ScrapeInfo(models.Model):
    external_id = models.CharField('External ID', unique=True, max_length=60, null=True)
    created = models.DateTimeField('Created Timestamp', auto_now_add=True)
    modified = models.DateTimeField('Modified Timestamp', auto_now=True)
    last_scraped = models.DateTimeField(
        'Last Scrpaed Timestamp', null=True, blank=True)
    scrape_count = models.IntegerField('Scrape Count', default=0)

    __prev_scrape_count = None

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__prev_scrape_count = self.scrape_count

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        if self.__prev_scrape_count != self.scrape_count:
            self.last_scraped = timezone.now()
        self.modified = timezone.now()
        super(ScrapeInfo, self).save(*args, **kwargs)
        self.__prev_scrape_count = self.scrape_count

    class Meta:
        abstract = True
