from . import seed_pages


def test_run():
    res = seed_pages.get_wiki_seed_pages(['Kategorie:Deutschsprachiges_Medium'])
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
