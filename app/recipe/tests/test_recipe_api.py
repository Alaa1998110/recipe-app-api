
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status
from ..serializers import RecipeSerializer,RecipeDetailSerializer
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from core.models import Recipe


RECIPES_URL=reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """create and return recipe detail that is dynamic"""
    return reverse('recipe:recipe-detail', args=[recipe_id])

def create_recipe(user,**params):
    """create and return a sample recipe"""
    defaults = {
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)
    recipe = Recipe.objects.create(user=user,**defaults)
    return recipe

class PublicRecipeApiTests(TestCase):
    """test unauthenticated API requests"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """test authentication is required for api"""
        res=self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """test authenticated API requests"""
    def setUp(self):
        self.client = APIClient()
        self.user=get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        create_recipe(user=self.user)
        create_recipe(user=self.user)
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer=RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_get_recipe_detail(self):
        recipe = create_recipe(user=self.user)
        url = detail_recipe(recipe_id)
        res=self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data,serializer.data)

