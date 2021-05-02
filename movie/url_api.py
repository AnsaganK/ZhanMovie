from django.conf.urls import url

from movie.views import MovieListApi, MovieDetailApi, MovieRandomDetailApi

urlpatterns = [
    url(r'^movies/$', MovieListApi.as_view()),
    url(r'^movies/(?P<pk>[0-9]+)/$', MovieDetailApi.as_view()),
    url(r'^movies/random', MovieRandomDetailApi.as_view()),
]
