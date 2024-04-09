from django.shortcuts import render
from rest_framework import viewsets
from .models import Actor, Tag, Movie, Rating
from .serializers import ActorSerializer, TagSerializer, MovieSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from authentication.permissions import IsRecommenderSystemAdmin

# Create your views here.
class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAuthenticated, IsRecommenderSystemAdmin]
    authentication_classes = [TokenAuthentication]


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated, IsRecommenderSystemAdmin]
    authentication_classes = [TokenAuthentication]


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, IsRecommenderSystemAdmin]
    authentication_classes = [TokenAuthentication]


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]