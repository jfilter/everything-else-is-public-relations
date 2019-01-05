import logging
from datetime import datetime, timedelta

import feedparser
import requests

logger = logging.getLogger(__name__)

ignore_titles = [
    "comments for",
    "comments on",
    "kommentare zu",
    "kommentare für",
    "commenti a",
]


def check_feed(feed_string, url):
    """filter out old or useless feeds
    """
    try:
        r = {"url": url}
        d = feedparser.parse(feed_string)
        if d.version:
            r["version"] = d.version
        if not "feed" in d:
            return None
        if "title" in d["feed"]:
            title = d["feed"]["title"]
            # don't save RSS for comments
            if any(title.lower().startswith(x) for x in ignore_titles):
                return None
            r["title"] = title
        if "entries" in d:
            # at least 3 articles in the last 90 days
            last_three_month = datetime.now() - timedelta(days=90)
            entries = [
                e
                for e in d.entries
                if hasattr(e, "published_parsed")
                and e.published_parsed is not None
                and datetime(*e.published_parsed[:6]) > last_three_month
            ]
            if len(entries) <= 3:
                return None
            text_array = sum([[e.title, e.description] for e in entries], [])
            if not is_german(text_array):
                return None

            oldest_item = min(
                [
                    datetime(*e.published_parsed[:6])
                    for e in d.entries
                    if hasattr(e, "published_parsed") and e.published_parsed is not None
                ]
            )

            time_difference = datetime.now() - oldest_item
            time_difference_in_days = time_difference / timedelta(days=1)
            r["posts_per_day"] = len(entries) / time_difference_in_days

        else:
            return None
        if "description" in d["feed"]:
            r["description"] = d["feed"]["description"]
        if "link" in d["feed"]:
            r["link"] = d["feed"]["link"]
        return r
    except Exception as e:
        logger.error(f"problem with checking feed: {input} {url}, {str(e)}")
        return None


def is_german(arr):
    r = requests.post("http://lang-ident.app.vis.one/german", data={"text": arr})
    if r.ok:
        return r.json()["isGerman"]
    return False
