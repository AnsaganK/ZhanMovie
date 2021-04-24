from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, redirect

from movie.forms import MovieForm, ReviewForm, UserForm, CategoryForm, GenreForm
from movie.models import Category, Movie, Genre, Country, Review, Role


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
                   "genres": genres, "best_movies": best_movies, "countries": countries})


def get_right_url_youtube(link):
    return link.replace('https://www.youtube.com/watch?v=', '')


def movie_detail(request, pk):
    user = request.user
    movie = Movie.objects.get(pk=pk)

    if (user.is_anonymous and movie.subscription == True):
        return render(request, "errorPage.html")
    if not user.is_anonymous:
        if (user.profile.role.name_en == "No subscription" and movie.subscription == True):
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
            return redirect("/category/{}".format(category.int))
        else:
            print(form.errors)
    genres = Genre.objects.all()
    categories = Category.objects.all()
    countries = Country.objects.all()
    return render(request, 'movie_add.html', {"categories": categories, "genres": genres, "countries": countries})


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
            role = Role.objects.filter(name_en="No subscription").first()
            if not role:
                role = Role.objects.create(name_ru="Без подписки", name_en="No subscription", name_kk="Жазылым жоқ")
            user.profile.role = role
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("index")
        else:
            return render(request, "registration/signup.html",
                          {"userNameFound": userNameFound, "passwordCheck": passwordCheck, "emailFound": emailFound})
    else:
        return render(request, "registration/signup.html")


def cabinet(request):
    user = request.user
    return render(request, 'cabinet.html', {"user": user})


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
    return render(request, "subscription.html")
