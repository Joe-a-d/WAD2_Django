import django_filters
from .models import *

class DogFilter(django_filters.FilterSet):

    #filters
    breed = django_filters.AllValuesMultipleFilter(field_name="breed", label="Breed")
    size = django_filters.AllValuesMultipleFilter(field_name="size", label="Size")
    age = django_filters.AllValuesMultipleFilter(field_name="age", label="Age")
    energyLevel = django_filters.AllValuesMultipleFilter(field_name="energyLevel", label="Personality")

    #sorters
    order = django_filters.OrderingFilter(fields=['favourites', 'score', 'created_at'])

    class Meta:
        model = Dog
        fields = ['breed', 'size', 'age', 'energyLevel',]
                    #'popularity', 'score', 'created_at']
