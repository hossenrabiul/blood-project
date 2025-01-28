
from django.urls import path , include
from rest_framework.routers import DefaultRouter

from .views import EventView


router = DefaultRouter()
router.register('events',EventView,basename='events')

urlpatterns = [
    path('',include(router.urls))
]
