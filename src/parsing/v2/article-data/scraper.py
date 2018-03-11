import requests
from bs4 import BeautifulSoup
import psycopg2
import json
import requests_cache
from crazy_urls import crazy_urls
from short_urls import short_urls
import sys
from parser import saved_ids

requests_cache.install_cache('demo_cache')

conn = psycopg2.connect(dbname="thoreventutturen", user="", password="")

def get_unique_urls():
    query = "select distinct url from adressa2.events"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return [row[0] for row in rows]

def get_meta(soup, meta):
    return soup.html.head.find("meta", attrs={ meta['key']: meta['val'] })

def fetch_page(url):
    if '.ece' not in url and '.html' not in url:
        return {
            'url': None,
            'page': None
        }

    urls = short_urls(url) + [url] + crazy_urls(url)
    success_url = False
    page = None
    for crazy_url in urls:
        print('# - trying :', crazy_url)
        page = requests.get(crazy_url)
        if page.status_code == 404:
            continue
        else:
            success_url = crazy_url
            break

    # save page to a file
    return {
        'url': crazy_url,
        'page': page
    }

def find_id_from_url(url):
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


def parse_page(page):
    soup = BeautifulSoup(page.text, 'html.parser')

    tags = {
        'title': [{ 'key': "property", 'val': "og:title"}],
        'url': [{ 'key': "property", 'val': "og:url"}],
        'description': [
            { 'key': "property", 'val': "og:description"},
            { 'key': "name", 'val': "description"},
        ],
        'image': [{ 'key': "property", 'val': "og:image"}],
        'published_time': [{ 'key': "property", 'val': "article:published_time"}],
        'modified_time': [{ 'key': "property", 'val': "article:modified_time"}],
        'author': [{ 'key': "property", 'val': "article:author"}],
        'articleId': [{ 'key': "name", 'val': "cXenseParse:recs:articleid"}],
    }
    data = {}

    for tag_key in tags:
        val = None
        for meta in tags[tag_key]:
            val = get_meta(soup, meta)
            if val != None:
                break
        if val is not None:
            data[tag_key] = val['content']

    # get the body
    body_content = soup.html.body.find("div", attrs={ "class": "body" })
    if body_content:
        data['content'] = body_content.text

    # get article id from url
    if 'articleId' not in data and 'url' in data:
        print('missing article id:', data['url'])
        data['articleId'] = find_id_from_url(data['url'])
        if not data['articleId'].isdigit():
            x = input('press to continue: ' + data['articleId'])

    return data


def main(start = 0, stop = 0):
    some_urls = []
    if start == -1:
        some_urls = get_unique_urls()
        start = 0
    elif stop <= start:
        print('# - Wrong input arguments')
        return
    else:
        some_urls = get_unique_urls()[start:stop]

    # get ids from the folder
    ids = saved_ids()

    print('NUMBER OF IDS:', len(ids))
    x = input('click to continue')

    for i, url in enumerate(some_urls):

        new_id = find_id_from_url(url)

        if new_id in ids:
            continue

        # skip shitty articles
        if 'boligguiden' in url or 'polarismedia.no' in url or 'int-ece5-4' in url or 'atb.no' in url:
            continue

        index = i + start
        print('fetching article', index, '|' + url + '|')
        res = fetch_page(url)
        if res['url'] is None:
            continue
        data = parse_page(res['page'])

        if 'url' not in data:
            print('What is wrong with this url', res['url'])
            continue

        # save the page to file
        with open('./data/' + data['articleId'] + '.html', 'w') as f:
            f.write(res['page'].text)


if __name__ == "__main__":
   main(int(sys.argv[1]), int(sys.argv[2]))
