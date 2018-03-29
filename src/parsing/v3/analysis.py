# pylint: disable=E1127

import pandas as pd
import numpy as np
import os
from math import floor


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


def user_item_sparse(df):
    ''' Return a sparse user item matrix '''
    df.reset_index(inplace=True)
    df.drop("ItemRating", 1, inplace=True)

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
    multi_df.to_csv("data/user_item_lookup.csv")

    # Return the User/Item matrix subset of the dataframe
    return (merge_df.loc[:, "ItemIndex":"UserIndex"])


if __name__ == "__main__":
    training_file = "data/training.csv"
    test_file = "data/test.csv"

    f_training_file = "data/training_dataframe.csv"
    f_test_file = "data/test_dataframe.csv"

    # Load the traing and test data as multiindex dataframes
    train_df = init_dataframe(training_file, f_training_file)
    test_df = init_dataframe(test_file, f_test_file)

    # Get a User/Item matrix from the training data
    user_item_matrix_df = user_item_sparse(train_df)
