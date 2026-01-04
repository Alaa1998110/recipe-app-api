
from drf_spectacular.utils import (extend_schema,extend_schema_view,OpenApiParameter,OpenApiTypes)
from rest_framework import (viewsets , mixins,status)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from recipe.serializers import (RecipeSerializer,RecipeDetailSerializer,TagSerializer)
from core.models import (Recipe ,Tag,Ingredient)
from rest_framework.decorators import action
from rest_framework.response import Response
from recipe.serializers import ( TagSerializer , IngredientSerializer,RecipeImageSerializer)

@extend_schema_view(
    list= extend_schema(
        parameters=[
            OpenApiParameter(
                'tags',
                OpenApiTypes.STR,
                description='Comma Separated list of IDs to filter ',
            ),
            OpenApiParameter(
                'ingredients',
                OpenApiTypes.STR,
                description='Comma Separated list of IDs to filter ',
            )
        ]
    )
)
class RecipeViewSet(viewsets.ModelViewSet):
    """ class manage recipe apis"""
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def _params_to_ints(self, qs):
        """convert a list of string into int"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """retrieve the recipes of the authenticated user"""
        tags=self.request.query_params.get('tags')
        ingredients=self.request.query_params.get('ingredients')
        queryset=self.queryset
        if tags:
            tag_ids=self._params_to_ints(tags)
            queryset=queryset.filter(tags__id__in=tag_ids)
        if ingredients:
            ingredient_ids=self._params_to_ints(ingredients)
            queryset=queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(
            user=self.request.user,
        ).order_by('-id').distinct()


    def get_serializer_class(self):
        """return the serializer class for request"""
        if self.action == 'list':
            return RecipeSerializer
        elif self.action == 'upload_image':
            return RecipeImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """create a new recipe"""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self,request,pk=None):
        """upload image to recipe"""
        recipe = self.get_object()
        serializer=self.get_serializer(recipe,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

class TagViewSet(BaseRecipeAttrViewSet):
    """manage tags in db"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()



class IngredientViewSet(BaseRecipeAttrViewSet):
    """manage ingredients in db"""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()



