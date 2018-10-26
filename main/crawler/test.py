from . import crawler, feed
from .. import util

# def test_run():
#     # res = crawler.get_links('https://netzpolitik.org/', 0)
#     res = crawler.crawl('https://netzpolitik.org/')
#     print(res)


# def test_fds():
#     res = crawler.get_links('https://fragdenstaat.de/blog/feed/', 0)
#     print(res)

# def test_feed():
#     res = feed.check_feed('http://www.sobla.de/service/webcms/newslistrss?componentID=4d6766d8-5465-41a8-a585-ab6454c8add0&pageID=105366-6993c8fe93bcdf55f57aea950247fac7', 'http://www.sobla.de/service/webcms/newslistrss?componentID=4d6766d8-5465-41a8-a585-ab6454c8add0&pageID=105366-6993c8fe93bcdf55f57aea950247fac7')
#     print(res)

# https://de.wikipedia.org/wiki/Kategorie:Deutschsprachiges_Medium
# https://de.wikipedia.org/wiki/Kategorie:Deutschsprachige_Tageszeitung
# https://de.wikipedia.org/wiki/Kategorie:Deutschsprachige_Zeitung
# https://de.wikipedia.org/wiki/Kategorie:Deutschsprachige_Wochenzeitung
# https://de.wikipedia.org/wiki/Kategorie:Deutschsprachige_Monatszeitung
# https://de.wikipedia.org/wiki/Kategorie:Deutschsprachige_Zeitung_im_Ausland
# https://de.wikipedia.org/wiki/Kategorie:Onlinemagazin
# https://de.wikipedia.org/wiki/Kategorie:Online-Journalismus
# https://de.wikipedia.org/wiki/Kategorie:Weblog
# https://de.wikipedia.org/wiki/Kategorie:Politik-Website

def test_feed_out_of_date():
    url = 'http://feeds.4players.de/-/game/4791/rss.xml'

    res = feed.check_feed(util.fetch(url).text, url)
    assert res is None


def test_feed_true():
    url = 'https://fragdenstaat.de/blog/feed/'

    res = feed.check_feed(util.fetch(url).text, url)
    assert not res is None

    print(res['posts_per_day'])
    assert res['posts_per_day'] > 0


def test_feed_lang_english():
    url = 'https://themoscowtimes.com/feeds/news.xml'

    res = feed.check_feed(util.fetch(url).text, url)
    assert res is None


def test_feed_days():
    url = 'http://am-mag.de/?feed=rss2'

    res = feed.check_feed(util.fetch(url).text, url)
    assert res is None
