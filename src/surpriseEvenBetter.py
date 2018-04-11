from surprise import Dataset
from surprise import Reader
from surprise import KNNBasic
from surprise import SVD
from sklearn.model_selection import KFold
from surprise.model_selection import cross_validate



if __name__ == '__main__':
    reader = Reader(line_format='user item rating', sep=',')

    data = Dataset.load_from_file('dataset1.data', reader=reader)


    def testKNNbasic(data):
        #data = Dataset.load_from_file('dataset1.data', reader=reader)

        sim_options = {'name' : 'cosine',
               'user_based' : True}

        algo = KNNBasic(sim_options=sim_options)
        cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=2, verbose=True)


    def testSVD():
        data = Dataset.load_from_file('dataset1.data', reader=reader)
        print("data")
        print(data)

        kf = KFold(n_splits=3)
        kf.get_n_splits(data)
        temp = kf.split(["a","aa","aba"])

        algo = SVD()
        for trainset, testset in temp:
            algo.fit(trainset)
            predictions = algo.test(testset)

    #testKNNbasic(data)
    testSVD()