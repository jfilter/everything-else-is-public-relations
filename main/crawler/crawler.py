import logging
from urllib import parse

from lxml import html

from . import feed
from .. import util

logger = logging.getLogger(__name__)


def crawl(start_url, max_depth=2):
    error_occured = False
    done = set()
    urls = [(start_url, 0)]
    i = 0

    # the concrete links
    feeds = []

    # collect all possible feed urls
    rss = set()
    atom = set()

    # loop over urls
    while len(urls) > i:
        url, depth = urls[i]

        # skip over element if it was already processed
        if url in done:
            i += 1
            continue

        result = get_links(url, depth)

        # skip over page if an error occured
        if result is None:
            error_occured = True
            i += 1
            continue

        new_urls, new_atom, new_rss, res_feed = result

        done.add(url)
        rss.update(new_rss)
        atom.update(new_atom)

        if not res_feed is None:
            feeds.append(res_feed)

        # all add new urls if the depth is not too much
        if depth < max_depth:
            urls += new_urls

        i += 1

    # only check / parse the links once
    for x in list(rss) + list(atom):
        res = util.fetch(x)
        if not res.ok:
            continue
        res_feed = feed.check_feed(res.text, x)
        if not res_feed is None:
            feeds.append(res_feed)

    return feeds, error_occured


def get_links(url, depth):
    logger.debug(f"fetch: {url}, {depth}")
    page = util.fetch(url)

    if page is None:
        logger.debug(f'something went wrong with this page: {url}')
        return None

    # check if the fetched page is actually a feed
    feed_types = ['text/xml', 'application/xml', 'rss+xml', 'atom+xml']
    res_feed = None
    if 'content-type' in page.headers:
        if any(x in page.headers['content-type'] for x in feed_types):
            res_feed = feed.check_feed(page.content, url)

    # so crawl links from it
    tree = html.fromstring(page.content)
    atom = tree.xpath('//a[@type="application/atom+xml"]/@href') + tree.xpath('//link[@type="application/atom+xml"]/@href')
    rss = tree.xpath('//a[@type="application/rss+xml"]/@href') + tree.xpath('//link[@type="application/rss+xml"]/@href')

    # often the feed urls are relative
    atom = util.create_abs_urls(atom, url)
    rss = util.create_abs_urls(rss, url)

    all_urls = tree.xpath('//a/@href')

    internal_urls = util.internal_urls(all_urls, url)

    # increase the depth
    return [(u, depth + 1) for u in internal_urls], atom, rss, res_feed
