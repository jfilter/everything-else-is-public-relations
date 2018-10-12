# import the logging library
import logging
import time
from urllib import parse

import requests

# Get an instance of a logger
logger = logging.getLogger(__name__)

# horrible code


def fetch(url, max_tries=5):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"}
    cur_try = 0
    while cur_try < max_tries:
        try:
            response = requests.get(url, headers=headers, timeout=30)
            # for 4xx, return instantly because another requests does not make sense
            if 400 <= response.status_code < 500:
                return None
            if 500 <= response.status_code < 600:
                response.raise_for_status()
            return response
        except:
            cur_try += 1
            time.sleep(cur_try * 10)  # increase sleep
    return None


def create_abs_urls(urls, base_url):
    return [parse.urljoin(base_url, l) for l in urls]


# https://stackoverflow.com/a/12170628/4028896
# removed the 'rss' extension because we are looking for it
IGNORED_EXTENSIONS = [
    # images
    'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
    'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',

    # audio
    'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

    # video
    '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
    'm4a',

    # other
    'css', 'pdf', 'doc', 'exe', 'bin', 'zip', 'rar',
]


def internal_urls(urls, base_url):
    res = set()

    urls = create_abs_urls(urls, base_url)
    orig_loc = parse.urlparse(base_url).netloc

    for u in urls:
        parsed = parse.urlparse(u)

        if not parsed.netloc == orig_loc:
            continue

        if any(parsed.path.endswith('.' + x) for x in IGNORED_EXTENSIONS):
            logger.debug(f'skip link: {u}')
            continue

        # normalized use only scheme, netloc and path
        normalized = parse.urlunparse(parsed[:3] + ('', '', ''))
        res.add(normalized)

    return list(res)


def external_base_urls(links):
    """Filter from Wikipedia pages extracted links
    """
    # filter all internal links
    links = [l for l in links if any(l.startswith(scheme) for scheme in ('//', 'http', 'https'))]

    res = []
    for l in links:
        parsed = parse.urlparse(l)
        netloc = parsed.netloc
        if any(wiki in netloc for wiki in ('wikipedia', 'wikidata', 'wikimedia', 'mediawiki')):
            logger.debug(f'skip: {l}')
            continue

        if any(parsed.path.endswith('.' + x) for x in IGNORED_EXTENSIONS):
            logger.debug(f'skip: {l}')
            continue

        base = parse.urlunparse(parsed[:2] + ('', '', '', ''))
        res.append(base)
    return list(set(res))  # unique
