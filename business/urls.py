from django.urls import path, include
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter

from business import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)
router.register('tasks', views.TaskViewSet)
router.register('business', views.BusinessViewSet)

app_name = 'business'

urlpatterns = [
    path('', include(router.urls))
]