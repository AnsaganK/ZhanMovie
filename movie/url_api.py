from django.conf.urls import url

from movie.views import MovieListApi, MovieDetailApi, MovieRandomDetailApi, CategoryListApi, GenreListApi

urlpatterns = [
    url(r'^movies/$', MovieListApi.as_view()),
    url(r'^movies/(?P<pk>[0-9]+)/$', MovieDetailApi.as_view()),
    url(r'^movies/random', MovieRandomDetailApi.as_view()),
    url(r'^category/$', CategoryListApi.as_view()),
    url(r'^categories/$', CategoryListApi.as_view()),
    url(r'^genres/$', GenreListApi.as_view()),
]
