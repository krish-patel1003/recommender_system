from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActorViewSet, TagViewSet, MovieViewSet, RatingViewSet

router = DefaultRouter()
router.register('actors', ActorViewSet)
router.register('tags', TagViewSet)
router.register('movies', MovieViewSet)
router.register('ratings', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]