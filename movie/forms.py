from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Movie, Review


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        exclude = ('url',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ('user','movie')

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',)
