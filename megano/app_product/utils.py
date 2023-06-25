import random

from django.db.models import QuerySet, Count, Avg, Max
from django.http import QueryDict

from app_product.models import Product


def apply_filters_to_queryset(queryset: QuerySet, params: QueryDict) -> QuerySet:
    """
    Applying filters to queryset
    :param queryset: Queryset object for filtering
    :param params: Params from user's request
    :return: Filtered queryset
    """

    if params:
        if params.get('filter[name]'):
            queryset = queryset.filter(title__icontains=params.get('filter[name]'))

        if params.get('filter[freeDelivery]') == 'true':
            queryset = queryset.filter(freeDelivery=True)

        if params.get('filter[available]') == 'true':
            queryset = queryset.filter(count__gt=0)

        if params.get('filter[minPrice]'):
            queryset = queryset.filter(price__gte=params.get('filter[minPrice]'))

        if params.get('filter[maxPrice]'):
            queryset = queryset.filter(price__lte=params.get('filter[maxPrice]'))

    sort_by = params.get('sort', 'date')
    sort_type = params.get('sortType', 'dec')
    queryset = queryset.annotate(
        reviews=Count('reviews_all'),
        rating=Avg('reviews_all__rating')
    ).order_by(
        f'{"-" if sort_type == "dec" else ""}{sort_by}'
    )

    category = params.get('category', None)
    if category:
        queryset = queryset.filter(category__id=category)

    tags = params.getlist('tags[]', None)
    if tags:
        queryset = queryset.filter(tags__id__in=tags)

    return queryset

def get_random_products() -> list:
    """
    Generates two random products
    :return: List with two random products
    """

    max_id = Product.objects.aggregate(max_id=Max("id"))['max_id']
    first_pk, second_pk = random.sample([num for num in range(1, max_id + 1)], 2)
    random_products = [Product.objects.get(pk=first_pk),
                       Product.objects.get(pk=second_pk)]
    return random_products

def pagination_for_items(params: QueryDict, count: int) -> tuple:
    """
    Create pagination for a certain number of items
    :param params: Parameters limit and current page
    :param count: Count of items
    """

    limit = int(params.get('limit', 20))
    last_page = (count // limit) + (1 if count % limit > 0 else 0)

    page = int(params.get('currentPage', 1))
    start = (page - 1) * limit
    end = start + limit

    return start, end, page, last_page