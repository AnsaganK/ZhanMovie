from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Movie, Review, Category, Genre


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = ('url',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user', 'movie')


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name_ru", "name_en", "name_kk")


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ("name_ru", "name_en", "name_kk")
