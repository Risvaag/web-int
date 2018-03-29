
import numpy as np
import pandas as pd
import pandas.io.sql as psql
import sqlite3 as sql
from time import time


def load_frame_from_database(database_loc, sql_query):
    ''' Load sqlite3 database into a dataframe, based on query '''

    con = sql.connect(database_loc)
    df = psql.read_sql_query(sql_query, con)
    con.close()
    return df


def train_and_test(df, msk_size=0.8):
    ''' Take in a dataframe and return two dataframes, one with test data, and one with training data based on the mask size'''
    msk = np.random.rand(len(df)) < msk_size
    return df[msk], df[~msk]


def store_train_and_test(train, test):
    ''' Store test and training data to csv files for ease of access later '''
    train.to_csv("data/training.csv", sep="\t", index=False)
    test.to_csv("data/testing.csv", sep="\t", index=False)


def split_and_store(df):
    ''' Split data into traning and test data, and store said data into csv files '''
    train, test = train_and_test(df)
    store_train_and_test(train, test)


if __name__ == "__main__":
    start_time = time()

    rating_headers = ['User', 'Item', 'ItemRating']

    df = load_frame_from_database(
        "data/adressa.sql", "SELECT USER_ID, URL, ACTIVE_TIME FROM event WHERE URL <> '' AND ACTIVE_TIME > 0")

    # Name the colums to improve readability
    df.columns = rating_headers

    split_and_store(df)

    print("Parsing the data took a total of {} seconds".format(time() - start_time))
