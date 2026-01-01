from core.models import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'link', 'time_minutes', 'price')
        read_only_fields = ('id',)