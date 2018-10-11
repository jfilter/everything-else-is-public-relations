
import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from .crawler import crawler
from .models import (
    STATUS_ERROR, STATUS_SUCCESS, STATUS_WAITING, STATUS_WORKING, Feed, SeedWikiWebsite, Website, WikiCategory,
)
from .seed import seed_pages

logger = logging.getLogger(__name__)


@db_periodic_task(crontab(minute='*'))
def cron_crawl():
    site_to_fetch = Website.objects.filter(status=STATUS_WAITING).first()
    if site_to_fetch:
        site_to_fetch.status = STATUS_WORKING
        site_to_fetch.save()

        logger.debug('start' + site_to_fetch.url)

        feeds, error = crawler.crawl(site_to_fetch.url)

        logger.debug('finish' + feeds + error)

        if error:
            site_to_fetch.status = STATUS_ERROR
        else:
            site_to_fetch.status = STATUS_SUCCESS
        site_to_fetch.save()

        if feeds is not None:
            for f in feeds:
                Feed.objects.get_or_create(website=site_to_fetch, **f)


@db_periodic_task(crontab(minute='*'))
def cron_websites():
    site_to_fetch = SeedWikiWebsite.objects.filter(status=STATUS_WAITING).first()
    if site_to_fetch:
        try:
            urls = seed_pages.extract_links_wiki_page(site_to_fetch.url)
            site_to_fetch.status = STATUS_SUCCESS
            if urls is not None:
                for url in urls:
                    Website.objects.get_or_create(url=url)

        except:
            logger.error('error with wiki extract websites: ' + site_to_fetch.text)
            site_to_fetch.status = STATUS_ERROR
        finally:
            site_to_fetch.save()


@db_periodic_task(crontab(minute='*'))
def cron_wiki_seed():
    cat_to_fetch = WikiCategory.objects.filter(status=STATUS_WAITING).first()
    if cat_to_fetch:
        try:
            urls = seed_pages.get_wiki_seed_pages(cat_to_fetch.text)
            cat_to_fetch.status = STATUS_SUCCESS
            if urls is not None:
                for url in urls:
                    SeedWikiWebsite.objects.get_or_create(url=url)

        except:
            logger.error('error with wiki seed: ' + cat_to_fetch.text)
            cat_to_fetch.status = STATUS_ERROR
        finally:
            cat_to_fetch.save()
