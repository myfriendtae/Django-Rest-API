from django.urls import path, include
from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('feed', views.UserProfileFeedViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('test-api/', views.HelloApiView.as_view()),
    path('login/', views.UserLoginApiView.as_view()),
    path('movie/', views.MovieApiView),
]
