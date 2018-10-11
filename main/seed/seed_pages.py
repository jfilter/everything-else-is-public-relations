
from urllib.parse import urlparse

import category_members
from lxml import html

from .. import util


def extract_links_wiki_page(url):
    """Extract links from wikipedia page
    """
    page = util.fetch(url)
    if page is None:
        return None
    tree = html.fromstring(page.content)
    links = tree.xpath('//a/@href')
    return util.external_base_urls(links)


def get_wiki_seed_pages(cat):
    """Get seed pages by extracting links from Wikipedia pages listed under specific categories
    """
    urls = category_members.retrieve(cat, mw_instance='https://de.wikipedia.org', types=['page'])
    urls = [u['link'] for u in urls]
    return urls
