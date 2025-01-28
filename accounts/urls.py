from django.urls import path , include
from rest_framework.routers import DefaultRouter

from .serializers import ProfileSerializers
from .views import UserRegistrationApiView,activate,UserLoignView,UserLogoutView,ProfileView,UserView

router = DefaultRouter()
router.register('profiles',ProfileView,basename='profiles')
router.register('users',UserView,basename='user')

urlpatterns = [
    path('register/',UserRegistrationApiView.as_view(), name='register'),
    path('active/<uid64>/<token>',activate,name='activate'),
    path('login/',UserLoignView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('',include(router.urls))
]