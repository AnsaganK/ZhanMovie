from rest_framework import serializers
from .models import *

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'year', 'subscription', 'poster')


class MovieDetailSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    countries = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    reviews = ReviewSerializer(many=True)
    class Meta:
        model = Movie
        exclude = ('draft', )

