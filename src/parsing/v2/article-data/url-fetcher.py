import json
import psycopg2

def get_unique_urls():
    query = "select distinct url from adressa2.events"
    conn = psycopg2.connect(dbname="thoreventutturen", user="", password="")
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return [row[0] row in rows]
