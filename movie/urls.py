from django.contrib.auth import views as acc
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('category/<int:pk>', category, name="category"),
    path('movies/<int:pk>', movie_detail, name="movie_detail"),
    path('movie_delete/<int:pk>', movie_delete, name="movie_delete"),
    path('movie_add/', movie_add, name="movie_add"),
    path('movie_update/<int:pk>', movie_update, name="movie_update"),
    path('movie_add_archive/<int:pk>', movie_add_archive, name="movie_add_archive"),
    path('movie_remove_archive/<int:pk>', movie_remove_archive, name="movie_remove_archive"),
    path('search/', search, name="search"),
    path('genre_delete/<int:pk>', genre_delete, name="genre_delete"),
    path('review_add/<int:pk>', review_add, name="review_add"),
    path('cabinet/', cabinet, name="cabinet"),
]

urlpatterns += [
    path('settings/categories', settings_categories, name="settings_categories"),
    path('settings/genres', settings_genres, name="settings_genres"),
    path('settings/movies', settings_movies, name="settings_movies"),
    path('settings/archive', settings_archive, name="settings_archive"),
    path('settings/actors', settings, name="settings_actors"),
    path('settings/producers', settings, name="settings_producers"),
    path('settings/users', settings_users, name="settings_users"),
]

urlpatterns += [
    path('accounts/signup', signup, name="signup"),
    path('accounts/login/', acc.LoginView.as_view(), name='login'),
    path('accounts/logout/', acc.LogoutView.as_view(), name='logout'),
    path('accounts/password-reset', acc.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-change/done/', acc.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password-change', acc.PasswordChangeView.as_view(), name='password_change'),
]
