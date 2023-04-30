from django.contrib import admin
from .models import Genre, Filmwork, GenreFilmwork, Person, PersonFilmwork


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ('full_name',)


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    fk_name = 'film_work'
    autocomplete_fields = ('genre', 'film_work',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    fk_name = 'film_work'
    autocomplete_fields = ('person', 'film_work',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (GenreFilmworkInline, PersonFilmworkInline)

    # Отображение полей в списке
    list_display = ('title', 'type', 'creation_date', 'rating',)

    # Фильтрация в списке
    list_filter = ('type', 'rating',)

    # Поиск по полям
    search_fields = ('title', 'description', 'id',)
