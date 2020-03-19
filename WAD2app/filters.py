import django_filters
from . import models

class DogFilter(django_filters.FilterSet):

    #filters
    breed = django_filters.AllValluesMultipleFilter(field_name="breed", label="Breed")
    size = django_filters.AllValluesMultipleFilter(field_name="size", label="Size")
    age = django_filters.AllValluesMultipleFilter(field_name="age", label="Age")
    pers = django_filters.AllValluesMultipleFilter(field_name="personality", label="Personality")
    garden = django_filters.AllValluesMultipleFilter(field_name="garden", label="Garden Required")

    #sorters
    order = filters.OrderingFilter(fields=['favourites', 'score', 'created_at']


    class Meta:
        model = Dog
        fields = ['breed', 'size', 'age', 'personality', 'garden',
                    'popularity', 'score', 'created_at']
