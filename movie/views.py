import git
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework import viewsets

from movie.forms import MovieForm, ReviewForm, UserForm, CategoryForm, GenreForm, MovieImageForm, UserEditForm, \
    ProfileForm
from movie.models import Category, Movie, Genre, Country, Review, Role, HistoryUser
from movie.serializers import MovieSerializer


def index(request):
    categories = Category.objects.all()
    best_movies = Movie.objects.filter(best=True).filter(archive=False)
    return render(request, 'index.html', {'categories': categories, "best_movies": best_movies})


# def general_page(request):

def category(request, pk):
    categories = Category.objects.all()
    category = categories.get(pk=pk)
    movies = category.movies.filter(archive=False)
    years = movies.values('year').distinct()
    genres = Genre.objects.all()
    countries = Country.objects.all()
    best_movies = Movie.objects.filter(best=True).filter(archive=False)
    genres_filter = [int(i) for i in request.GET.getlist("genre")]
    year_filter = [int(i) for i in request.GET.getlist("year")]
    country_filter = [int(i) for i in request.GET.getlist("country")]
    if movies:
        showFilter = True
    else:
        showFilter = False
    if request.GET:
        showFilter = True
        if request.GET.getlist("genre"):
            movies = movies.filter(Q(genres__in=request.GET.getlist("genre"))
                               ).distinct()
        if request.GET.getlist("year"):
            movies = movies.filter(Q(year__in=request.GET.getlist("year")))
        if request.GET.getlist("country"):
            movies = movies.filter(
                                   Q(countries__in=request.GET.getlist("country")))
    paginator = Paginator(movies, 8)
    page = request.GET.get('page')
    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)

    return render(request, 'category.html',
                  {'categories': categories, 'categoryName': category.name, "movies": query, "years": years,
                   "genres": genres, "best_movies": best_movies, "countries": countries, "showFilter": showFilter,
                   "genres_filter": genres_filter, "year_filter": year_filter, "country_filter": country_filter})


def get_right_url_youtube(link):
    return link.replace('https://www.youtube.com/watch?v=', '')


def movie_detail(request, pk):
    user = request.user
    movie = Movie.objects.get(pk=pk)
    if movie.subscription:
        if user.is_anonymous:
            return render(request, "errorPage.html")
        if not user.profile.subscription and not user.profile.admin:
            return render(request, "errorPage.html")
    video_link = None
    if movie.video_url:
        video_link = get_right_url_youtube(movie.video_url)

    genresIds = movie.genres.all().values('id')
    countriesIds = movie.countries.all().values('id')
    genresIds = [i["id"] for i in genresIds]
    countriesIds = [i["id"] for i in countriesIds]
    categories = Category.objects.all()
    genres = Genre.objects.all()
    countries = Country.objects.all()
    reviews = movie.reviews.all()
    if not user.is_anonymous:
        history = HistoryUser.objects.filter(user=user)
        if (history and history.first().movie != movie) or not history:
            h = HistoryUser(user=user, movie=movie)
            h.save()
    return render(request, 'movie_detail.html',
                  {'movie': movie, "video_link": video_link,
                   'genresIds': genresIds, 'countriesIds': countriesIds,
                   "categories": categories, "genres": genres, "countries": countries, 'reviews': reviews})


def movie_add(request):
    if request.method == "POST":
        post = request.POST
        form = MovieForm(post, request.FILES)
        category = Category.objects.get(pk=post["category"])
        if form.is_valid():
            movie = form.save()
            for i in post:
                if i.split("_")[0] == 'country':
                    country = Country.objects.get(pk=int(i.split("_")[1]))
                    movie.countries.add(country)
                if i.split("_")[0] == 'genre':
                    genre = Genre.objects.get(pk=int(i.split("_")[1]))
                    movie.genres.add(genre)
            if 'title_en' in post:
                print(post)
                movie.url = str(post['title_en']) + "_" + str(movie.pk)
            else:
                movie.url = str(movie.pk)
            movie.save()
            return redirect("/category/{}".format(category.pk))
        else:
            print(form.errors)
    genres = Genre.objects.all()
    categories = Category.objects.all()
    countries = Country.objects.all()
    return render(request, 'movie_add.html', {"categories": categories, "genres": genres, "countries": countries})


def add_movie_image(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.method == "POST":
        form = MovieImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save()
            data.movie = movie
            data.save()
    return redirect(movie.get_absolute_url())


def movie_update(request, pk):
    if request.method == "POST":
        movie = Movie.objects.get(pk=pk)
        movie.genres.clear()
        movie.countries.clear()
        post = request.POST
        form = MovieForm(post, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            for i in post:
                if i.split("_")[0] == 'country':
                    country = Country.objects.get(pk=int(i.split("_")[1]))
                    movie.countries.add(country)
                if i.split("_")[0] == 'genre':
                    genre = Genre.objects.get(pk=int(i.split("_")[1]))
                    movie.genres.add(genre)
            if 'title_en' in post:
                movie.url = str(post['title_en']) + "_" + str(movie.pk)
            else:
                movie.url = str(movie.pk)
            movie.save()
            return redirect(movie.get_absolute_url())
        else:
            print(form.errors)


def movie_add_archive(request, pk):
    movie = Movie.objects.get(pk=pk)
    movie.archive = True
    movie.save()
    return redirect(movie.get_absolute_url())


def movie_remove_archive(request, pk):
    movie = Movie.objects.get(pk=pk)
    movie.archive = False
    movie.save()
    return redirect(movie.get_absolute_url())


def movie_delete(request, pk):
    movie = Movie.objects.get(pk=pk)
    category = movie.category
    movie.delete()
    return redirect('/category/{}'.format(category.pk))

def movie_delete_for_settings(request, pk):
    movie = Movie.objects.get(pk=pk)
    category = movie.category
    movie.delete()
    return redirect('/settings/movies')

def subscription_add(request):
    user = request.user
    if user.is_authenticated:
        user.profile.subscription = True
        user.save()
    return redirect('/cabinet')


def subscription_delete(request):
    user = request.user
    if user.is_authenticated:
        user.profile.subscription = False
        user.save()
    return redirect('/cabinet')


def settings(request):
    return render(request, 'settings.html')


def settings_categories(request):
    categories = Category.objects.all()
    return render(request, 'settings_page/category.html', {"categories": categories})


def settings_genres(request):
    genres = Genre.objects.all()
    return render(request, 'settings_page/genres.html', {"genres": genres})


def settings_movies(request):
    movies = Movie.objects.filter(archive=False)
    return render(request, 'settings_page/movies.html', {'movies': movies})


def settings_archive(request):
    movies = Movie.objects.filter(archive=True)
    return render(request, 'settings_page/movies.html', {"movies": movies})


def settings_users(request):
    users = User.objects.all()
    return render(request, 'settings_page/users.html', {"users": users})


def settings_roles(request):
    roles = Role.objects.all()
    return render(request, 'settings_page/roles.html', {"roles": roles})


def settings_other(request):
    return render(request, 'settings_page/other.html')


def search(request):
    q = request.GET.get('q')
    data = Movie.objects.filter(
        Q(title__icontains=q) | Q(description__icontains=q) | Q(tagline__icontains=q))

    paginator = Paginator(data, 8)
    page = request.GET.get('page')
    try:
        query = paginator.page(page)
    except PageNotAnInteger:
        query = paginator.page(1)
    except EmptyPage:
        query = paginator.page(paginator.num_pages)

    return render(request, 'search_result.html', {"data": query, "query": q})


def review_add(request, pk):
    movie = Movie.objects.get(pk=pk)
    isReview = Review.objects.filter(user=request.user, movie=movie)
    if isReview:
        return redirect(movie.get_absolute_url())
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.movie = movie
            data.save()
        else:
            print(form.errors)
    return redirect(movie.get_absolute_url())


def userNameValid(username):
    user = User.objects.filter(username=username)
    if user:
        return True
    return False


def emailValid(email):
    user = User.objects.filter(email=email)
    if user:
        return True
    return False


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        userNameFound = userNameValid(request.POST["username"])
        emailFound = emailValid(request.POST["email"])
        passwordCheck = request.POST["password1"] != request.POST["password2"]
        if form.is_valid() and not (emailFound or passwordCheck):
            user = form.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("index")
        else:
            return render(request, "registration/signup.html",
                          {"userNameFound": userNameFound, "passwordCheck": passwordCheck, "emailFound": emailFound})
    else:
        return render(request, "registration/signup.html")


def cabinet(request):
    user = request.user
    history = HistoryUser.objects.filter(user=user)[:8]
    reviews = user.reviews.all()[:8]
    return render(request, 'cabinet.html', {"user": user, "history": history, "reviews": reviews})

def edit_user(request):
    user = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
        form2 = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form2.is_valid():
            form2.save()
        else:
            print(form.errors)

        return redirect('/cabinet')
    return render(request, "edit.html", {"user": user})


def category_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    return redirect("/settings/categories")


def category_delete(request, pk):
    category = Category.objects.get(pk=pk)
    category.delete()
    return redirect("/settings/categories")


def genre_add(request):
    if request.method == "POST":
        form = GenreForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect("/settings/genres")


def genre_delete(request, pk):
    genre = Genre.objects.get(pk=pk)
    genre.delete()
    return redirect('/settings/genres')


def subscription(request):
    user = request.user
    if user.is_anonymous:
        return render(request, "registration/login.html")
    return render(request, "subscription.html")


def update_pull(request):
    if request.method == 'POST':
        repo = git.Repo('https://github.com/AnsaganK/ZhanMovie')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer