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




def SVDAlgo():

    data = Dataset.load_from_file('dataset1.data', reader=reader)
    # data = Dataset.load_builtin('ml-100k')

    # define a cross-validation iterator
    kf = KFold(n_splits=5)

    algo = SVD()

    for trainset, testset in kf.split(data):
        # train and test algorithm.
        algo.fit(trainset)
        predictions = algo.test(testset)

        # Compute and print Root Mean Squared Error
        accuracy.rmse(predictions, verbose=True)

def KNNBasicAlgo(userID, instanceID, trueRating, k=5):
    data = Dataset.load_from_file('smallerDataset1.data', reader=reader)

    #kf = KFold(n_splits=3)
    trainset = data.build_full_trainset()

    algo = KNNBasic(k=k, sim_options={'name':'cosine', 'user_based':False})
    algo.fit(trainset)

    prediction = algo.predict(userID, instanceID, trueRating, verbose=True)
    #algo.fit(trainset).test(testset)
if __name__ == '__main__':
    #SVDAlgo()
    KNNBasicAlgo("cx:iol0os2i30xf6xbc:enn7ciik36v3","9d615dd08d92c8e9670fb72b5c78cbc6b52501c4", 11)