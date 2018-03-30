# pylint: disable=E1127
# pylint: disable=E0401

import pandas as pd
import numpy as np
import scipy.sparse as sp
import sklearn.preprocessing as pp

import os
import sys

from sklearn.metrics.pairwise import cosine_similarity
from math import floor
from time import time
from scipy.io import mmread, mmwrite


def init_dataframe(raw_data_file, formatted_file):
    if os.path.isfile(formatted_file):
        print("Formatted file found. Loading data...")
        return pd.read_csv(formatted_file, sep="\t", index_col=[0, 1])
    else:
        print("No formatted file found. Indexing data and creating a new file")
        df = pd.read_csv(raw_data_file, sep="\t", index_col=[0, 1])
        df.groupby(level=[0, 1]).sum()
        df.sort_index(level='User', ascending=False, inplace=True)
        df.to_csv(formatted_file, sep="\t")

    return df


def user_item_sparse(df, file):
    ''' Return a sparse user item matrix '''
    df.reset_index(inplace=True)
    # df.drop("ItemRating", 1, inplace=True)

    # Create and store the item lookup dataframe
    items = pd.DataFrame(df.Item.unique(), columns=["Item"])
    items.reset_index(level=0, inplace=True)
    items.columns = ["ItemIndex", "Item"]

    # Create and store the user lookup dataframe
    users = pd.DataFrame(df.User.unique(), columns=["User"])
    users.reset_index(level=0, inplace=True)
    users.columns = ["UserIndex", "User"]

    # Merge the user ids and item ids into the dataframe
    tmp_df = pd.merge(df, items, left_on=["Item"], right_on=["Item"])
    merge_df = pd.merge(tmp_df, users, left_on=["User"], right_on=["User"])

    # Convert the dataframe to a multiindex df to remove duplicate compound indexes
    multi_df = merge_df.set_index(["UserIndex", "ItemIndex"], inplace=False)
    multi_df = multi_df[~multi_df.index.duplicated(keep="first")]

    # Store the multiindex in a csv so we can find the user ids and article urls later
    multi_df.reset_index(inplace=True)

    multi_df = multi_df[["UserIndex", "ItemIndex",
                         "ItemRating", "User", "Item"]]
    multi_df.to_csv(file, sep="\t")

    # Return the User/Item matrix subset of the dataframe
    return (multi_df.loc[:, "ItemIndex":"ItemRating"])


def load_or_fetch_ui(df, file):
    if os.path.isfile(file):
        print("Loading pre-existing User/Item Matrix...")
        df = pd.read_csv(file, sep="\t")
        df = df[["UserIndex", "ItemIndex", "ItemRating", "User", "Item"]]
        return (df.loc[:, "UserIndex":"ItemRating"])
    else:
        print("File not found. Creating User/Item Matrix")
        return user_item_sparse(df, file)


def get_ratings(df):
    n_users = df.UserIndex.unique().shape[0]
    n_items = df.ItemIndex.unique().shape[0]

    print("Creating a ({} X {}) matrix and filling it.".format(
        n_users, n_items))

    start_time = time()
    ratings = np.zeros((n_users, n_items))

    for row in df.itertuples():
        ratings[row[1], row[2]] = row[3]

    sparse_ratings = sp.csc_matrix(ratings)

    print("Finished loading the ratings, after about {} seconds".format(
        int(time()-start_time)))
    return sparse_ratings


def load_or_fetch_ratings(df, file):
    if os.path.isfile(file + ".mtx"):
        print("Loading ratings from file.")
        return mmread(file + ".mtx")
    else:
        print("File not found. Creating sparse rating matrix.")
        while True:
            verif = input(
                "This is potentially taxing on memory. Are you sure you want to proceed? (y/n): ")

            if verif.lower() in ["y", "yes"]:
                ratings = get_ratings(df)
                mmwrite(file, ratings)
                return ratings
            elif verif.lower() in ["n", "no"]:
                sys.exit(1)


def chunking_dot(mat_a, mat_b chunk_size=100):
    # Make a copy if the array is not already contiguous
    R = np.empty((mat_a.shape[0], mat_b.shape[0]))
    print(R.shape)
    for i in range(0, R.shape[0], chunk_size):
        end = i + chunk_size

        print(
            "Progress: {}% ({}/{}".format(floor(end/R.shape[0]), end, R.shape[0]))
        R[i:end] = np.dot(mat_a[i:end], mat_b)
    return R


if __name__ == "__main__":
    training_file = "data/training.csv"
    test_file = "data/test.csv"

    f_training_file = "data/training_dataframe.csv"
    f_test_file = "data/test_dataframe.csv"

    # Load the traing and test data as multiindex dataframes
    train_df = init_dataframe(training_file, f_training_file)
    # test_df = init_dataframe(test_file, f_test_file)

    # Get a User/Item matrix from the training data
    user_item_df = load_or_fetch_ui(train_df, "data/user_item_lookup.csv")

    # Create a user item rating matrix
    ratings = load_or_fetch_ratings(user_item_df, "data/ratings")

    # Calculate user-similarities
    rating_norm = pp.normalize(ratings.tocsc(), axis=0)
    #similarities = rating_norm * rating_norm.T

    rating_matrix = rating_norm.toarray()
    similarity = chunking_dot(rating_matrix, rating_matrix.T, chunk_size=1000)

    #sim = ratings.dot(ratings.T).toarray()
    # print(sim)

    #rating_norm = cosine_similarity(ratings, dense_output=False)

    # print(user_similarities)
