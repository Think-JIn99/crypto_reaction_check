from vader_feature import new_words
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
    'site',
    'earn',
    'project',
    'check'
    ]
    
include_words = [
    'price','crypto',
    'currency','money',
    'BTC','bitcoin','bit',
    'ETH','ether','ethereum',
    'XRP','ripple',
    'DOGE','doge',
    'coin','market','elon','musk',
    'fed','powell'
    ]
url_patt = r"(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}"
nan_patt = r"(^.?removed.?$)|(^.?deleted.?$)" #결측치 제거용
def get_word_patt(is_remove = True):
    if is_remove:
        words = remove_words
    else:
        include_words.extend(new_words.keys())
        words = include_words
    word_patt = [r"\b" + w + r"+(\w{1,3})?\b" for w in words]
    word_patt = "|".join(word_patt)
    return [word_patt]
