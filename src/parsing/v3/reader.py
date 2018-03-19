import pandas as pd
import pandas.io.sql as pd_sql
import json
from models import Event, val, stop
import os.path

skipped = 0


def is_loaded(file, tracker):
    with open(tracker, 'r') as f:
        data = json.load(f)
        if file in data:
            return True
        return False


def add_loaded(file, tracker):
    with open(tracker, 'w+') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            data = {}

        data[file] = True

        json.dump(data, f)


def read_file(file, tracker):
    global skipped

    if not os.path.isfile(file):
        print("Make sure you add the data files to a /data folder inside the v3 folder and run the python script again!")
        return

    if is_loaded(file, tracker):
        print("{} already loaded".format(file))
        return

    with open(file) as f:
        line_number = 0

        for line in f:
            data = json.loads(line)

            url = val(data, 'url')
            if '.html' not in url and '.ece' not in url:
                skipped += 1
                continue

            Event.put(data)

            if line_number % 5000 == 0:
                print('We are on: ', line_number, 'skipped: ', skipped)
            line_number += 1

    add_loaded(file, tracker)
    print("Finished loading file {}".format(file))


def addPath(file):
    return "data/" + file


if __name__ == "__main__":
    filenames = list(map(addPath, ["20170101", "20170102", "20170103",
                                   "20170104", "20170105", "20170106",
                                   "20170107"]))
    filetracker = "complete.json"

    read_file(filenames[0], filetracker)
    stop()
