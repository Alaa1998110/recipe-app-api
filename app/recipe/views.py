
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import RecipeSerializer
from core.models import Recipe


class RecipeViewSet(viewsets.ModelViewSet):
    """ class manage recipe apis"""
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        """retrieve the recipes of the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')