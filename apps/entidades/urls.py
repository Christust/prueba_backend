from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.entidades import views

router = DefaultRouter()

router.register(r"", views.MaestroViewSet)

urlpatterns = [] + router.urls
