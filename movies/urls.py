from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActorViewSet, TagViewSet, MovieViewSet, RatingViewSet

router = DefaultRouter()
router.register('actors', ActorViewSet, basename='actors')
router.register('tags', TagViewSet, basename='tags')
router.register('movies', MovieViewSet, basename='movies')
router.register('ratings', RatingViewSet, basename='ratings')

urlpatterns = [
    path('', include(router.urls)),
]