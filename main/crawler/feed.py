import logging
from datetime import timedelta, datetime
from collections import Counter

import feedparser
from pyfasttext import FastText


logger = logging.getLogger(__name__)

ignore_titles = ['comments for', 'comments on', 'kommentare zu', 'kommentare für', 'commenti a']


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
            title = d['feed']['title']
            # don't save RSS for comments
            if any(title.lower().startswith(x) for x in ignore_titles):
                return None
            r['title'] = title
        if 'entries' in d:
            # at least 3 articles in the last 90 days
            last_three_month = datetime.now() - timedelta(days=90)
            entries = [e for e in d.entries if e.published_parsed is not None and datetime(*e.published_parsed[:6]) > last_three_month]
            if len(entries) <= 3:
                return None
            text_array = sum([[e.title, e.description] for e in entries], [])
            if not is_german(text_array):
                return None
        else:
            return None
        if 'description' in d['feed']:
            r['description'] = d['feed']['description']
        if 'link' in d['feed']:
            r['link'] = d['feed']['link']
        return r
    except Exception as e:
        logger.error(f'problem with checking feed: {input} {url}, {str(e)}')
        return None


model = FastText('/lid.176.bin')
# model = FastText('lid.176.bin')


def is_german(arr):
    preds = sum(predict_lang(arr), [])

    # check if the most common is german
    return Counter(preds).most_common(1)[0][0] == 'de'


def predict_lang(arr):
    return model.predict(arr)
