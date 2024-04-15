from rest_framework import serializers
from .models import Actor, Tag, Movie, Rating
from django.contrib.auth.models import User


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'
    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):

    actors = ActorSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Movie
        fields = '__all__'
    
    def create(self, validated_data):
        print("Create method called")
        actors_data = validated_data.pop('actors')
        tags_data = validated_data.pop('tags')
        movie = Movie.objects.create(**validated_data)
        for actor_data in actors_data:
            actor, created = Actor.objects.get_or_create(**actor_data)
            movie.actors.add(actor)
        for tag_data in tags_data:
            print(tag_data)
            tag, created = Tag.objects.get_or_create(**tag_data)
            movie.tags.add(tag)
        return movie


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
    
    
    
