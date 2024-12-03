import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import GridSearchCV
import logging

logging.basicConfig(level=logging.INFO)


def train_model():
    rating = pd.read_csv(
        '/Users/zakariyapolevchishikov/PycharmProjects/MLiRS/AIProject/MLrec/services/dataset/ratings.csv')
    reader = Reader(rating_scale=(0.5, 5))
    data = Dataset.load_from_df(rating[['userId', 'movieId', 'rating']], reader)

    param_grid = {'n_factors': [50, 100], 'lr_all': [0.002, 0.005], 'reg_all': [0.02, 0.1]}
    gs = GridSearchCV(SVD, param_grid, measures=['rmse'], cv=3)
    gs.fit(data)

    best_algo = gs.best_estimator['rmse']
    best_algo.fit(data.build_full_trainset())
    return best_algo


def get_user_recommendations(user_id, algo):
    movies = pd.read_csv(
        '/Users/zakariyapolevchishikov/PycharmProjects/MLiRS/AIProject/MLrec/services/dataset/movies.csv')
    ratings = pd.read_csv(
        '/Users/zakariyapolevchishikov/PycharmProjects/MLiRS/AIProject/MLrec/services/dataset/ratings.csv')

    user_ratings = ratings[ratings['userId'] == user_id]
    watched_movies = user_ratings['movieId'].tolist()

    all_movie_ids = movies['movieId'].tolist()
    unseen_movies = [movie for movie in all_movie_ids if movie not in watched_movies]

    predictions = []
    for movie_id in unseen_movies:
        pred = algo.predict(user_id, movie_id)
        predictions.append((movie_id, pred.est))

    predictions.sort(key=lambda x: x[1], reverse=True)
    top_movie_ids = [pred[0] for pred in predictions[:10]]

    recommended_movies = movies[movies['movieId'].isin(top_movie_ids)]

    return recommended_movies
