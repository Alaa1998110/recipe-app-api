
from rest_framework import (viewsets , mixins)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe.serializers import (RecipeSerializer,RecipeDetailSerializer,TagSerializer)
from core.models import (Recipe ,Tag)

from recipe.serializers import TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """ class manage recipe apis"""
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        """retrieve the recipes of the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """return the serializer class for request"""
        if self.action == 'list':
            return RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """create a new recipe"""
        serializer.save(user=self.request.user)

class TagViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """manage tags in db"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        """retrieve the tags of the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')