from django.urls import path, include
from . import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test-api/', views.HelloApiView.as_view())
]
