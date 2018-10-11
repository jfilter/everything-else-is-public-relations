import logging

import feedparser

logger = logging.getLogger(__name__)


def check_feed(feed_string, url):
    # takes string as well as URLs as input
    try:
        r = {'url': url}
        d = feedparser.parse(feed_string)
        if d.version:
            r['version'] = d.version
        if d['feed']['title']:
            r['title'] = d['feed']['title']
        if d['feed']['description']:
            r['description'] = d['feed']['description']
        if d['feed']['link']:
            r['link'] = d['feed']['link']
        return r
    except Exception as e:
        logger.error(f'problem with checking feed: {input} {url}, {str(e)}')
        return None
