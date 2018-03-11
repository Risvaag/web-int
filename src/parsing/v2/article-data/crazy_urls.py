

def cap_words(s, index = 0):
    all_words = []
    def rec(s, index = 0):
        if index >= len(s):
            all_words.append(s)
            return
        # return one with title
        with_title = s[:]
        with_title[index] = s[index].capitalize()
        rec(with_title, index + 1)
        # and one without title
        rec(s[:], index + 1)
    # kick it all off
    rec(s)
    return all_words

def crazy_urls(url):
    if '-' not in url or '.ece' not in url:
        return []
    last_part = url.split('.ece')[0].split('/')[-1]
    first_part = url.split('.ece')[0].split('/')[:-1]

    ending = 'ece' + url.split('.ece')[1]
    words = last_part.split('-')
    article_id = words[-1]
    words.pop()

    # we wont handle words will really long titles - its a waste of time
    if len(words) > 10:
        return []

    words = [word.lower() for word in words]

    urls = []
    for word_combo in cap_words(words):
        new_url = '/'.join(first_part) + '/' + '-'.join(word_combo) + '-' + article_id + '.' + ending
        urls.append(new_url)

    return urls
