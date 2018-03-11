def id_from_url(url):
    if ('-') in url:
        if 'b.html' in url:
            return url.split('b.html')[0].split('-')[-1]
        if '.ece' in url:
            return url.split('.ece')[0].split('-')[-1]
        if '.html' in url:
            return url.split('.html')[0].split('-')[-1]

    if '.html' in url:
        part = url.split('.html')[0].split('/')[-1]
        return ''.join([s for s in part if s.isdigit()])

    if '.ece' in url:
        part = url.split('.ece')[0].split('/')[-1]
        return ''.join([s for s in part if s.isdigit()])

    return 0
