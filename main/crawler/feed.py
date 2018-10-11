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
        if not 'feed' in d:
            return None
        if 'title' in d['feed']:
            r['title'] = d['feed']['title']
        if 'description' in d['feed']:
            r['description'] = d['feed']['description']
        if 'link' in d['feed']:
            r['link'] = d['feed']['link']
        return r
    except Exception as e:
        logger.error(f'problem with checking feed: {input} {url}, {str(e)}')
        return None
