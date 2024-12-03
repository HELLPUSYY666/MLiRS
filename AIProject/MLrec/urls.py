from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('recommendations/<int:user_id>/', views.user_recommendations_view, name='user_recommendations'),
]
