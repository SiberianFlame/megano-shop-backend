import django_filters


class AverageStars(django_filters.FilterSet):
    average_stars = django_filters.NumberFilter(field_name='average_stars', lookup_expr='lte')

    class Meta:
        model = None
        fields = ('average_stars',)