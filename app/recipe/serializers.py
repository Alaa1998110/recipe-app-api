from core.models import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id','link' ,'title', 'time_minutes', 'price')
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """serializer for recipe details"""
    class Meta(RecipeSerializer.Meta):
        fields= RecipeSerializer.Meta.fields + ('description',)
