from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse


class Category(models.Model):
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание", null=True, blank=True)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.url

    def get_absolute_url(self):
        return reverse('category', args=[str(self.pk)])

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание", null=True, blank=True)
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Producer(models.Model):
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.FileField("Изображение", upload_to="producers/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('producer_detail', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"


class Actor(models.Model):
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.FileField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"


class Movie(models.Model):
    title = models.CharField("Название", max_length=100, null=True, blank=True)
    tagline = models.CharField("Слоган", max_length=100, default='', null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    poster = models.FileField("Постер", upload_to="moviePoster/", null=True, blank=True)
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019, null=True, blank=True)
    country = models.CharField("Страна", max_length=30, null=True, blank=True)
    countries = models.ManyToManyField("Country", null=True, blank=True, related_name="movies")
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", null=True, blank=True,
                                       related_name="film_director")
    directors_list = models.TextField(null=True, blank=True)
    actors = models.ManyToManyField(Actor, verbose_name="актеры", null=True, blank=True, related_name="film_actor")
    actors_list = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, verbose_name="жанры", null=True, blank=True, related_name="movies")
    world_premiere = models.DateField("Премьера в мире", default=date.today, null=True, blank=True)
    best = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True, related_name='movies', blank=True
    )
    url = models.SlugField(max_length=130, unique=True, null=True, blank=True)
    draft = models.BooleanField("Черновик", default=False)
    video = models.FileField(upload_to="video/", null=True, blank=True)
    video_url = models.TextField(null=True, blank=True)

    archive = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"pk": self.pk})

    #    def get_review(self):
    #        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieImages(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Кадры из фильма", related_name="images")
    image = models.FileField(upload_to="movieImages")

    def __str__(self):
        return self.movie.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильмов"


class Country(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class Role(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True, related_name="profiles")
    photo = models.FileField(upload_to="photoUsers", null=True, blank=True, verbose_name="Фотография")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Review(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE, related_name="reviews", verbose_name="Пользователь")
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
