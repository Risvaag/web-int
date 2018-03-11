import glob
from bs4 import BeautifulSoup
import psycopg2
from id_from_url import id_from_url
import sys

conn = psycopg2.connect(dbname="thoreventutturen", user="", password="")


def get_meta(soup, meta):
    return soup.html.head.find("meta", attrs={ meta['key']: meta['val'] })

def val(data, key):
    if key in data:
        return data[key]
    return None


def parse_page(page_text):
    soup = BeautifulSoup(page_text, 'html.parser')

    # attributes to add

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
        data['articleId'] = id_from_url(data['url'])
        print('ARTICLE ID:', data['articleId'])
        if not data['articleId'].isdigit():
            x = input('press to continue: ' + data['articleId'])

    return data

def id_from_file(file_name):
    return file_name.split('.html')[0].split('/')[-1]

def saved_ids():
    files = glob.glob('./data/*.html')
    return [id_from_file(f) for f in files]

def read_file(name):
    content = None
    with open(name, 'r') as f:
        content = f.read()
    return content

i = 0

def save_data(data):
    global i
    query = """INSERT INTO data.articles (
      id,
      url,
      title,
      author,
      description,
      image,
      publushed_time,
      modified_time,
      category,
      keywords,
      body
    ) VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s,
        %s
    );
    """
    cursor = conn.cursor()
    insert_data = (
        val(data, 'articleId'),
        val(data, 'url'),
        val(data, 'title'),
        val(data, 'author'),
        val(data, 'description'),
        val(data, 'image'),
        val(data, 'published_time'),
        val(data, 'modified_time'),
        val(data, 'category'),
        val(data, 'keywords'),
        val(data, 'content'),
    )
    cursor.execute(query, insert_data)

    i += 1

    if i % 20 == 0:
        print('saving!')
        conn.commit()



def parse_all_saved_articles():
    print('parsing!')

    all_ids = saved_ids()

    for article_id in all_ids:
        text = read_file('./data/' + article_id + '.html')
        data = parse_page(text)
        #try:
        save_data(data)
        print('# - saved ', data['articleId'])
        #except:
        #    print('failed saving ', data['articleId'])
        #    print("Unexpected error:", sys.exc_info()[0])



if __name__ == "__main__":
    parse_all_saved_articles()
