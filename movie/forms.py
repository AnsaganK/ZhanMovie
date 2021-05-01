from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Movie, Review, Category, Genre, MovieImages, Profile


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = ('url',)


class MovieImageForm(forms.ModelForm):
    class Meta:
        model = MovieImages
        fields = ("image",)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user', 'movie')


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'photo')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name_ru", "name_en", "name_kk")


class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ("name_ru", "name_en", "name_kk")
