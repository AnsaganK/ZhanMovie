from modeltranslation.translator import register, TranslationOptions
from .models import Movie, Category, Genre, Role, Actor, Country, Producer

@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Role)
class RoleTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Producer)
class ProducerTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
