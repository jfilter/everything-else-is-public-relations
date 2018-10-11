from . import crawler


# def test_run():
#     # res = crawler.get_links('https://netzpolitik.org/', 0)
#     res = crawler.crawl('https://netzpolitik.org/')
#     print(res)


def test_fds():
    res = crawler.get_links('https://fragdenstaat.de/blog/feed/', 0)
    print(res)

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
