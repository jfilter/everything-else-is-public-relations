import time
from urllib import parse


import requests

# horrible code


def fetch(url, max_tries=10):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"}
    cur_try = 0
    while cur_try < max_tries:
        try:
            page = requests.get(url, headers=headers, timeout=30)
            break  # success
        except:
            cur_try += 1
            time.sleep(cur_try * 10)  # increase sleep
    return page


def internal_urls(urls, baseurl):
    res = set()
    urls = [parse.urljoin(baseurl, l) for l in urls]

    orig_loc = parse.urlparse(baseurl).netloc

    for u in urls:
        parsed = parse.urlparse(u)

        if not parsed.netloc == orig_loc:
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
            continue

        base = parse.urlunparse(parsed[:2] + ('', '', '', ''))
        res.append(base)
    return list(set(res))  # unique
