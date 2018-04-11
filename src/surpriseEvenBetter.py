from surprise import Dataset
from surprise import Reader
from surprise import KNNBasic
from surprise import SVD
from sklearn.model_selection import KFold
from surprise.model_selection import cross_validate
from surprise import accuracy
from surprise import SVD
from surprise import Dataset
from surprise import accuracy
from surprise.model_selection import KFold
from surprise import Reader

reader = Reader(line_format='user item rating', sep='\t')




def SVDalgo():

    data = Dataset.load_from_file('dataset1.data', reader=reader)
    # data = Dataset.load_builtin('ml-100k')

    # define a cross-validation iterator
    kf = KFold(n_splits=3)

    algo = SVD()

    for trainset, testset in kf.split(data):
        # train and test algorithm.
        algo.fit(trainset)
        predictions = algo.test(testset)

        # Compute and print Root Mean Squared Error
        accuracy.rmse(predictions, verbose=True)


if __name__ == '__main__':
    SVDalgo()