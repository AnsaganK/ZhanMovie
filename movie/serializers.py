from rest_framework import serializers
from .models import *


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'description', 'poster')
