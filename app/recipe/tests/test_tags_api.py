from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer



TAGS_URL = reverse('recipe:tag-list')
def detail_url(tag_id):
    """return detail url"""
    return reverse('recipe:tag-detail',args=[tag_id])

def create_user(email='test@example.com',password='testpass123'):
    """create new user"""
    return get_user_model().objects.create(email=email,password=password)

class PublicTagsApiTests(TestCase):
    """test unauthenticated api requests"""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """test authentication is required"""
        res=self.client.get(TAGS_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):
    """test authenticated api requests"""
    def setUp(self):
        self.client = APIClient()
        self.user=create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """test retrieve tags in a list"""
        Tag.objects.create(user=self.user,name='test tag')
        Tag.objects.create(user=self.user,name='other tag')
        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by('-name')
        serializer=TagSerializer(tags,many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_tags_limited_to_user(self):
        """test retrieving tags for authenticated user"""
        user2 = create_user(email='user2@example.com')
        Tag.objects.create(user=user2,name='test tag2')
        tag = Tag.objects.create(user=self.user,name='test tag')
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],tag.name)
        self.assertEqual(res.data[0]['id'],tag.id)

    def test_update_tag(self):
        """test updating a tag"""
        tag=Tag.objects.create(user=self.user,name='test tag')
        payload={'name':'new tag'}
        url = detail_url(tag.id)
        res=self.client.patch(url,payload)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name,payload['name'])

    def test_delete_tag(self):
        """test deleting a tag"""
        tag=Tag.objects.create(user=self.user,name='breakfast')
        url=detail_url(tag.id)
        res=self.client.delete(url)
        self.assertEqual(res.status_code,status.HTTP_204_NO_CONTENT)
        tags=Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())

