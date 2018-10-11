
from huey import crontab
from huey.contrib.djhuey import db_task, db_periodic_task

from . import models
from .crawler import crawler
from .seed import seed_pages


@db_periodic_task(crontab(minute='*'))
def cron_crawl():
    # limit number of crawling in parallel
    num_active_worksr = models.Website.objects.filter(status=models.STATUS_WORKING).count()
    if num_active_worksr >= 10:
        return

    site_to_fetch = models.Website.objects.filter(status=models.STATUS_WAITING).first()
    if site_to_fetch:
        site_to_fetch.status = models.STATUS_WORKING
        site_to_fetch.save()

        print('start', site_to_fetch.url)

        feeds, error = crawler.crawl(site_to_fetch.url)

        print('finish', feeds, error)

        if error:
            site_to_fetch.status = models.STATUS_ERROR
        else:
            site_to_fetch.status = models.STATUS_SUCCESS
        site_to_fetch.save()

        if feeds is not None:
            for f in feeds:
                models.Feed.objects.get_or_create(website=site_to_fetch, **f)


@db_periodic_task(crontab(minute='*'))
def cron_websites():
    site_to_fetch = models.SeedWikiWebsite.objects.filter(status=models.STATUS_WAITING).first()
    if site_to_fetch:
        try:
            urls = seed_pages.extract_links_wiki_page(site_to_fetch.url)
            site_to_fetch.status = models.STATUS_SUCCESS
            if urls is not None:
                for url in urls:
                    models.Website.objects.get_or_create(url=url)

        except:
            print('error with wiki extract websites', site_to_fetch.text)
            site_to_fetch.status = models.STATUS_ERROR
        finally:
            site_to_fetch.save()


@db_periodic_task(crontab(minute='*'))
def cron_wiki_seed():
    cat_to_fetch = models.WikiCategory.objects.filter(status=models.STATUS_WAITING).first()
    if cat_to_fetch:
        try:
            urls = seed_pages.get_wiki_seed_pages(cat_to_fetch.text)
            cat_to_fetch.status = models.STATUS_SUCCESS
            if urls is not None:
                for url in urls:
                    models.SeedWikiWebsite.objects.get_or_create(url=url)

        except:
            print('error with wiki seed', cat_to_fetch.text)
            cat_to_fetch.status = models.STATUS_ERROR
        finally:
            cat_to_fetch.save()
