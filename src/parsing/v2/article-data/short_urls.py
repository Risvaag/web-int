
def get_article_id(url):
    if '/article' in url:
        return url.split('/article')[1].split('.ece')[0].strip()
    return url.split('.ece')[0].split('-')[-1].strip()

def short_url(url):
    return 'https://www.adressa.no/article' + get_article_id(url) + '.ece'


def short_url_with_sections(url, sections):
    return 'https://www.adressa.no/' + '/'.join(sections) + '/article' + get_article_id(url) + '.ece'


def is_section(x_sec):
    sec = x_sec.strip()
    if sec.isdigit():
        return False
    if sec == 'http:' or sec == 'https:':
        return False
    if sec == '' or '.' in sec:
        return False
    return True

def get_sections(url):
    if '.html' in url or '.ece' not in url:
        return []

    all_sections = url.split('.ece')[0].split('/')[0:-1]

    return [sec for sec in all_sections if is_section(sec)]


def short_urls(url):
    if '.html' in url:
        return []
    urls = []
    sections = get_sections(url)
    if '.html' not in url and len(sections) > 0:
        urls.append(short_url_with_sections(url, sections))
    urls.append(short_url(url))
    return urls
