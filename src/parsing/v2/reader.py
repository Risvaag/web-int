import json
import psycopg2

conn = psycopg2.connect(dbname="thoreventutturen", user="", password="")
skipped = 0

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def val(data, key):
    if key in data:
        return data[key]
    return None


def read_file(name):
    global skipped
    with open('../data/' + name) as f:
        i = 1
        query = """INSERT INTO adressa2.events (
        active_time,
        author,
        canonical_url,
        category,
        city,
        country,
        device_type,
        event_id,
        cx_id,
        keywords,
        os,
        publishtime,
        referrer_host_class,
        referrer_search_engine,
        referrer_social_network,
        referrer_url,
        region,
        session_start,
        session_stop,
        cx_time,
        title,
        url,
        user_id
        ) VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s
        );
        """

        for line in f:
            data = json.loads(line.strip())
            url = val(data, 'url')
            if '.html' not in url and '.ece' not in url:
                skipped += 1
                continue

            cursor = conn.cursor()
            insert_data = (
                val(data, 'activeTime'),
                val(data, 'author'),
                val(data, 'canonicalUrl'),
                val(data, 'category1'),
                val(data, 'city'),
                val(data, 'country'),
                val(data, 'deviceType'),
                val(data, 'eventId'),
                val(data, 'id'),
                val(data, 'keywords'),
                val(data, 'os'),
                val(data, 'publishtime'),
                val(data, 'referrerHostClass'),
                val(data, 'referrerSearchEngine'),
                val(data, 'referrerSocialNetwork'),
                val(data, 'referrerUrl'),
                val(data, 'region'),
                val(data, 'sessionStart'),
                val(data, 'sessionStop'),
                val(data, 'time'),
                val(data, 'title'),
                val(data, 'url'),
                val(data, 'userId'),
            )
            cursor.execute(query, insert_data)

            if i % 5000 == 0:
                print([key for key in data])
                print('we are on: ', i, 'skipped: ', skipped)
                conn.commit()
            i += 1

#read_file('20170101')
read_file('20170102')
read_file('20170102')
read_file('20170103')
read_file('20170105')
read_file('20170106')
read_file('20170107')
