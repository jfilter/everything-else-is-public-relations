import feedparser


def check_feed(input, url):
    # takes string as well as URLs as input
    try:
        r = {'url': url}
        d = feedparser.parse(input)
        r['version'] = d.version
        r['title'] = d['feed']['title']
        r['description'] = d['feed']['description']
        r['link'] = d['feed']['link']
        return r
    except:
        return None
