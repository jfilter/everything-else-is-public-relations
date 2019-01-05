from . import get_info


def test_fds():
    url = 'https://fragdenstaat.de'
    res = get_info.get_info(url)

    assert not res is None
    print(res)
    assert(res[2] > 0)
