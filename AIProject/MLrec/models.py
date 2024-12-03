from django.db import models


class Movie(models.Model):
    movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    genres = models.TextField()

    def __str__(self):
        return self.title


class Rating(models.Model):
    user_id = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.user_id} -> {self.movie.title}: {self.rating}"
