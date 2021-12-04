remove_words = [
    'free',
    'install',
    'download',
    'app',
    'wallet',
    'hardware',
    'link',
    'card',
    'payapl',
    'mine',
    'platform',
    'browser',
    'site']
url_patt = r"(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}"
nan_patt = r"(^.?removed.?$)|(^.?deleted.?$)"
def get_word_patt():
    word_patt = [r"\b" + w + r"+(\w{1,2})?\b" for w in remove_words]
    word_patt = "|".join(word_patt)
    return [word_patt, url_patt, nan_patt]