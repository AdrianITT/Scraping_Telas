from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import scrape_modatelas_view


router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
     path('scrape/modatelas/', scrape_modatelas_view, name='scrape_modatelas_view'),
]