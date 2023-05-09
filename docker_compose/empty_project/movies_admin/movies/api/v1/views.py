from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.db.models import Q

from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        filmwork_queryset = Filmwork.objects.values('id', 'title', 'description', 'creation_date', 'rating', 'type') \
            .annotate(genres=ArrayAgg('genres__name', distinct=True),
                      actors=ArrayAgg('persons__full_name',
                                      filter=Q(personfilmwork__role='actor'), distinct=True),
                      directors=ArrayAgg('persons__full_name',
                                         filter=Q(personfilmwork__role='director'), distinct=True),
                      writers=ArrayAgg('persons__full_name',
                                       filter=Q(personfilmwork__role='writer'), distinct=True),
                      )

        return filmwork_queryset

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    model = Filmwork
    http_method_names = ['get']
    paginate_by = 50

    def get_context_data(self):
        queryset = list(self.get_queryset())
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset, self.paginate_by)

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.has_previous() and page.previous_page_number(),
            'next': page.has_next() and page.next_page_number(),
            'results': queryset,
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    model = Filmwork

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        context = {
            'results': queryset.filter(id=self.kwargs['pk']).get(),
        }
        return context
