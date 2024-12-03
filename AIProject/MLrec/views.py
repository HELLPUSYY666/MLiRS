from django.shortcuts import render
import pandas as pd
from .models import Movie, Rating
from django.shortcuts import render
from django.http import JsonResponse
from .services.ml_utilis import *


algo = train_model()


def user_recommendations_view(request, user_id):
    movies = pd.read_csv('/Users/zakariyapolevchishikov/PycharmProjects/MLiRS/AIProject/MLrec/services/dataset/movies.csv')
    recommendations = get_user_recommendations(user_id, algo)

    data = []
    for movie_id in recommendations['movieId']:
        movie = movies[movies['movieId'] == movie_id]
        if not movie.empty:
            data.append({"title": movie.iloc[0]['title'], "genres": movie.iloc[0]['genres']})

    return JsonResponse(data, safe=False)



def load_data():
    movies = pd.read_csv('services/dataset/movies.csv')
    ratings = pd.read_csv('services/dataset/ratings.csv')

    for _, row in movies.iterrows():
        Movie.objects.create(movie_id=row['movieId'], title=row['title'], genres=row['genres'])

    for _, row in ratings.iterrows():
        movie = Movie.objects.get(movie_id=row['movieId'])
        Rating.objects.create(user_id=row['userId'], movie=movie, rating=row['rating'])
