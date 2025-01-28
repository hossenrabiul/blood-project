import django_filters
from django_filters import FilterSet
from .models import Event

from .constraint import STATUS_CHOICES
from accounts.constraint import BLOOD_GROUP


class EventFilter(FilterSet):
    event_date = django_filters.DateFilter(field_name='event_date', lookup_expr='exact')
    status = django_filters.ChoiceFilter(choices= STATUS_CHOICES, lookup_expr='exact') 
    blood = django_filters.ChoiceFilter(field_name='blood', lookup_expr='exact')

    user = django_filters.NumberFilter(field_name='user_id', lookup_expr='exact')  # Filter by user
    doner = django_filters.NumberFilter(field_name='doner_id', lookup_expr='exact')  # Filter by doner
    event_id = django_filters.NumberFilter(field_name='id', lookup_expr='exact')  # Filter by event id

    class Meta:
        model = Event
        fields = ['event_id','blood','event_date', 'status', 'doner','user']


   