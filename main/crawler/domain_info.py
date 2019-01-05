from datetime import datetime, timedelta

from lxml import html

from . import util


def get_reddits_per_day(url):
    if url.startswith("https://"):
        url = url[len(("https://")) :]

    if url.startswith("http://"):
        url = url[len(("http://")) :]

    if url.startswith("//"):
        url = url[len(("//")) :]

    reddit_url = f"https://www.reddit.com/domain/{url}/new.json?sort=new"

    res = util.fetch(reddit_url)
    if res is None:
        return 0

    r_j = res.json()

    if not "data" in r_j or not "children" in r_j["data"]:
        return 0

    chil = r_j["data"]["children"]
    if len(chil) == 0:
        return 0

    last_date = datetime.fromtimestamp(chil[-1]["data"]["created_utc"])
    days = (datetime.now() - last_date) / timedelta(days=1)
    return len(chil) / days


def get_info(url):
    res = util.fetch(url)

    if res is None:
        return None

    doc = html.fromstring(res.content)

    title_element = doc.xpath("//title")

    website_title = (
        title_element[0].text_content().strip() if len(title_element) > 0 else ""
    )
    meta_description_element = doc.xpath("//meta[@name='description']/@content")
    website_meta_description = (
        meta_description_element[0].strip() if len(meta_description_element) > 0 else ""
    )

    return {
        "title": website_title,
        "description": website_meta_description,
        "reddits_per_day": get_reddits_per_day(url),
    }
