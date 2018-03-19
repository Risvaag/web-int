import os
import time
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

# Set up path to db
db = SqliteExtDatabase(os.path.dirname(
    os.path.abspath(__file__)) + "/data/adressa.sql")


class BaseModel(Model):
    class Meta:
        database = db


# Connect to database (instantiation)
db.connect()


def val(data, key):
    if key in data:
        return data[key]
    return None


def valInt(data, key):
    if val(data, key):
        return int(data[key])
    return None


class Event(BaseModel):
    EVENT_ID = TextField(unique=True)
    USER_ID = TextField()

    # Session data
    SESSION_START = TextField(null=True)
    SESSION_STOP = TextField(null=True)
    CX_TIME = IntegerField(null=True)
    ACTIVE_TIME = IntegerField(null=True)
    DEVICE_TYPE = TextField(null=True)
    OS = TextField(null=True)

    # Location fields
    COUNTRY = TextField(null=True)
    REGION = TextField(null=True)
    CITY = TextField(null=True)

    # Article fields
    URL = TextField(null=True)
    CANONICAL_URL = TextField(null=True)
    CX_ID = TextField(null=True)
    TITLE = TextField(null=True)
    AUTHOR = TextField(null=True)
    KEYWORDS = TextField(null=True)
    CATEGORY = TextField(null=True)
    PUBLISH_TIME = TextField(null=True)

    # Referrer fields
    REFERRER_URL = TextField(null=True)
    REFERRER_SEARCH_ENGINE = TextField(null=True)
    REFERRER_SOCIAL_NETWORK = TextField(null=True)
    REFERRER_HOST_CLASS = TextField(null=True)

    @staticmethod
    def put(data):
        try:
            Event(
                EVENT_ID=val(data, 'eventId'),
                USER_ID=val(data, 'userId'),
                SESSION_START=val(data, 'sessionStart'),
                SESSION_STOP=val(data, 'sessionStop'),
                CX_TIME=valInt(data, 'time'),
                ACTIVE_TIME=valInt(data, 'activeTime'),
                DEVICE_TYPE=val(data, 'deviceType'),
                OS=val(data, 'os'),
                COUNTRY=val(data, 'country'),
                REGION=val(data, 'region'),
                CITY=val(data, 'city'),
                URL=val(data, 'url'),
                CANONICAL_URL=val(data, 'canonicalUrl'),
                CX_ID=val(data, 'id'),
                TITLE=val(data, 'title'),
                AUTHOR=val(data, 'author'),
                KEYWORDS=val(data, 'keywords'),
                CATEGORY=val(data, 'category1'),
                PUBLISH_TIME=val(data, 'publishtime'),
                REFERRER_URL=val(data, 'referrerUrl'),
                REFERRER_SEARCH_ENGINE=val(data, 'referrerSearchEngine'),
                REFERRER_SOCIAL_NETWORK=val(data, 'referrerSocialNetwork'),
                REFERRER_HOST_CLASS=val(data, 'referrerHostClass'),
            ).save()
        except IntegrityError as e:
            pass
        except Exception as e:
            print('Failed to add {} due to {}'.format(data, e))


Event.create_table(True)


def stop():
    db.close()
