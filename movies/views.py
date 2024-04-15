from django.shortcuts import render
from rest_framework import viewsets
from .models import Actor, Tag, Movie, Rating
from .serializers import ActorSerializer, TagSerializer, MovieSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from authentication.permissions import IsRecommenderSystemAdmin
from rest_framework.decorators import action
from movies.utils import user_based_recommender_utils, movie_based_recommender_utils

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


class MovieViewSet(viewsets.ViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, IsRecommenderSystemAdmin]
    authentication_classes = [TokenAuthentication]

    def destroy(self, request, pk=None):
        instance = self.queryset.get(pk=pk)
        instance.delete()
        return Response({'message': 'Movie has been deleted'}, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        instance = self.queryset.get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs['pk'])
        serializer = self.serializer_class(instance)
        return Response(serializer.data)    

    @action(detail=False, methods=['GET'])
    def knnusers(self, request, *args, **kwargs):
        user = request.user
        recommended_movies = user_based_recommender_utils.knn_users_recommend_movies(user=user, n=3)
        return Response({'recommended_movies': recommended_movies, 'message': 'Movies has been recommended'}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['GET'])
    def knnmovies(self, request, *args, **kwargs):
        user = request.user
        movie = request.query_params.get('movie')
        suggested_users = movie_based_recommender_utils.knn_movies_suggest_users(user=user, movie=movie, n=3)
        return Response({'suggested_users': suggested_users, 'message': 'Movies has been recommended'}, status=status.HTTP_200_OK)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]