from django_filters.rest_framework import BaseInFilter, CharFilter, FilterSet

from reviews.models import Title


class CharFilterInFilter(BaseInFilter, CharFilter):
    pass


class TitleFilter(FilterSet):
    """A filter for Title instances."""

    genre = CharFilterInFilter(
        field_name='genre__slug',
        lookup_expr='in',
    )
    category = CharFilterInFilter(
        field_name='category__slug',
        lookup_expr='in',
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
