from surprise import KNNBasic
from surprise import Reader
from surprise import Dataset
from surprise import SVD
from sklearn.model_selection import KFold
import numpy as np


data = []

with open("dataset1.txt") as infile:
    for line in infile:
        splitted = line.split('--')
        data.append(splitted)

data = np.array(data)
print data


algo = SVD()

kf = KFold(n_splits=3)
kf.get_n_splits(data)


for trainset, testset in kf.split(data):
    algo.fit(trainset)
    predictions = algo.test(trainset)
