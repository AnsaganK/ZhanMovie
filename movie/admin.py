from django.contrib import admin
from .models import Movie, MovieImages, Profile, Genre, Category, Actor, Producer, Role, Country, Review

admin.site.register(MovieImages)
admin.site.register(Movie)
admin.site.register(Country)
admin.site.register(Role)
admin.site.register(Profile)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Actor)
admin.site.register(Producer)
admin.site.register(Review)
