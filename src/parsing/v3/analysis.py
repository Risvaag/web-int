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
from time import sleep
from scipy.io import mmread, mmwrite

LIMIT = 50000
CHUNK_SIZE = 500  # Should be a divisor of LIMIT


def init_dataframe(raw_data_file, formatted_file):
    if os.path.isfile(formatted_file):
        print("Loading dataframe from file.")
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
        print("Loading user/item matrix from file.")
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


def similarity_cosine_by_chunk(rating, start, end):
    if end > rating.shape[0]:
        end = rating.shape[0]

    return cosine_similarity(X=rating[start:end], Y=rating)


def chunked_similarities(rating, chunk_size=CHUNK_SIZE):
    R = np.empty((rating.shape[0], rating.shape[0]))

    for chunk_start in range(0, R.shape[0], chunk_size):
        cosine_similarity_chunk = similarity_cosine_by_chunk(
            rating, chunk_start, chunk_start+chunk_size)

        R[chunk_start: chunk_start + chunk_size] = cosine_similarity_chunk
        print("Finished frame {}/{}".format(chunk_start +
                                            chunk_size, rating.shape[0]))

    return R


def load_or_fetch_similarities(ratings, file):
    if os.path.isfile(file):
        print("Loading similarities from file.")
        return np.load(file)
    else:
        rating_norm = pp.normalize(ratings.tocsr(), axis=1)

        # Limit to 50k users (due to memory limitations)
        ratings_split = rating_norm[:LIMIT]
        rating_matrix = ratings_split.toarray()
        similarities = chunked_similarities(rating_matrix)
        np.save(file, similarities)
        return similarities


def get_user_index(df, num):
    return df[df.UserIndex == num]


def get_user_similarities(mat, num, thresh=0.01):
    for i in range(0, len(mat[num])):
        sim = mat[num][i]

        if sim >= thresh:
            print("User: {}, similarity: {}".format(i, sim))


def get_top_similar(mat, user, num=10):
    user_row = mat[user]
    indexes = np.argpartition(user_row, -num)[-num:]

    for i in range(0, len(indexes)):
        if indexes[i] == user:
            continue
        print("{}: User - {}, Similarity - {}%".format(i + 1,
                                                       indexes[i], floor(user_row[indexes[i]] * 100)))


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
    #print(get_user_index(user_item_df, 4))

    # Create a user item rating matrix
    ratings = load_or_fetch_ratings(user_item_df, "data/ratings")

    # Calculate user-similarities
    similarities = load_or_fetch_similarities(ratings, "data/similarities.npy")
    get_top_similar(similarities, 0)

    #get_user_similarities(similarities, 37752)
    # print(get_user_index(user_item_df, 0))
    # print(get_user_index(user_item_df, 37298))
