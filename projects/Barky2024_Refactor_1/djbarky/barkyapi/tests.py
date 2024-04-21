from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import routers
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Bookmark, Snippet
from .views import BookmarkViewSet, SnippetViewSet
from .serializers import UserSerializer, SnippetSerializer, BookmarkSerializer

# Create your tests here.


class BookmarkTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.bookmark = Bookmark.objects.create(
            id=1,
            title="Awesome Django",
            url="https://awesomedjango.org/",
            notes="Best place on the web for Django.",
        )
        # print(f"bookmark id: {self.bookmark.id}")

        # the simple router provides the name 'bookmark-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:bookmark-list")
        self.detail_url = reverse(
            "barkyapi:bookmark-detail", kwargs={"pk": self.bookmark.id}
        )

    # 1. create a bookmark
    def test_create_bookmark(self):
        """
        Ensure we can create a new bookmark object.
        """

        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Django REST framework",
            "url": "https://www.django-rest-framework.org/",
            "notes": "Best place on the web for Django REST framework.",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Bookmark.objects.count(), 2)
        self.assertEqual(Bookmark.objects.get(
            id=99).title, "Django REST framework")

    # 2. list bookmarks
    def test_list_bookmarks(self):
        """
        Ensure we can list all bookmark objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"]
                         [0]["title"], self.bookmark.title)

    # 3. retrieve a bookmark
    def test_retrieve_bookmark(self):
        """
        Ensure we can retrieve a bookmark object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], self.bookmark.title)

    # 4. delete a bookmark
    def test_delete_bookmark(self):
        """
        Ensure we can delete a bookmark object.
        """
        response = self.client.delete(
            reverse("barkyapi:bookmark-detail",
                    kwargs={"pk": self.bookmark.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bookmark.objects.count(), 0)

    # 5. update a bookmark
    def test_update_bookmark(self):
        """
        Ensure we can update a bookmark object.
        """
        # the full record is required for the POST
        data = {
            "id": 99,
            "title": "Awesomer Django",
            "url": "https://awesomedjango.org/",
            "notes": "Best place on the web for Django just got better.",
        }
        response = self.client.put(
            reverse("barkyapi:bookmark-detail",
                    kwargs={"pk": self.bookmark.id}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], "Awesomer Django")


class SnippetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            id=89,
            password="123_Pass*",
            last_login="2024-04-10 00:45:15",
            is_superuser="False",
            username='The One',
            last_name="Parent",
            email="theone@gmail.com",
            is_staff="False",
            is_active="True",
            date_joined="2023-04-01 00:45:15",
            first_name="Male"
        )

        self.factory = APIRequestFactory()
        saveuser = User.objects.get(username="The One")
        self.snippet = Snippet.objects.create(
            created="2024-04-15 10:11:12",
            title="Awesome snippet",
            code="example awesome snippet code",
            linenos="False",
            language="python",
            style="friendly",
            owner=saveuser,
            highlighted="code",
        )
        # print(f"snippet title: {self.snippet.title}")

        # the simple router provides the name 'snippet-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:snippet-list")
        self.detail_url = reverse(
            "barkyapi:snippet-detail", kwargs={"pk": self.snippet.title}
        )
    # 6. create a snippet

    def test_create_snippet(self):
        """
        Ensure we can create a new snippet object.
        """
        self.factory = APIRequestFactory()
        saveuser = User.objects.get(username="The One")

        # the full record is required for the POST
        data = {
            "created": "2024-04-15 09:12:18",
            "title": "Django REST framework",
            "code": "example snippet code",
            "linenos": "False",
            "language": "python",
            "style": "friendly",
            "owner": saveuser,
            "highlighted": "code",
        }
        response = self.client.post(self.list_url, data)
#        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Snippet.objects.count(), 1)
        self.assertEqual(response.data["title"], "Django REST framework")

    # 7. retrieve a snippet
    def test_retrieve_snippet(self):
        """
        Ensure we can retrieve a snippet object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], self.snippet.title)

    # 8. delete a snippet
    def test_delete_snippet(self):
        """
        Ensure we can delete a snippet object.
        """
        response = self.client.delete(
            reverse("barkyapi:snippet-detail",
                    kwargs={"pk": self.snippet.title})
        )
        # HTTP_403_Forbidden)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 1)

    # 9. list snippets
    def test_list_snippets(self):
        """
        Ensure we can list all snippet objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"]["title"], self.snippet.title)

    # 10. update a snippet
    def test_update_snippet(self):
        """
        Ensure we can update a snippet object.
        """
        self.factory = APIRequestFactory()
        saveuser = User.objects.get(username="The One")

        # the full record is required for the POST
        data = {
            "created": "2024-04-15 03:04:05",
            "title": "Even better Django",
            "code": "example snippet code",
            "linenos": "False",
            "language": "python",
            "style": "friendly",
            "owner": saveuser,
            "highlighted": "code",
        }
        response = self.client.put(
            reverse("barkyapi:snippet-detail",
                    kwargs={"pk": self.snippet.title}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["title"], "Even better Django")


class UserTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            id=105,
            password="123_Pass*",
            last_login="2023-04-10 01:02:00",
            is_superuser="False",
            username="The Great",
            last_name="Parent",
            email="thegreat@gmail.com",
            is_staff="False",
            is_active="True",
            date_joined="2023-04-01 06:08:09",
            first_name="Male"
        )
        # print(f"user username: {self.user.username}")

        # the simple router provides the name 'user-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:user-list")
        self.detail_url = reverse(
            "barkyapi:user-detail", kwargs={"pk": self.user.id}
        )

    # 11. create a user
    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """

        # the full record is required for the POST
        data = {
            "id": 115,
            "password": "123_Pass*",
            "last_login": "2024-04-15 11:15:58",
            "is_superuser": "False",
            "username": "The Best",
            "last_name": "Parent",
            "email": "thebest@gmail.com",
            "is_staff": "False",
            "is_active": "True",
            "date_joined": "2024-04-15 10:11:12",
            "first_name": "Female"
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=115).username, "The Best")

    # 12. retrieve a user
    def test_retrieve_user(self):
        """
        Ensure we can retrieve a user object.
        """
        response = self.client.get(self.detail_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["username"], self.user.username)

    # 13. delete a user
    def test_delete_user(self):
        """
        Ensure we can delete a user object.
        """
        response = self.client.delete(
            reverse("barkyapi:user-detail",
                    kwargs={"pk": self.user.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    # 14. list users
    def test_list_users(self):
        """
        Ensure we can list all user objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"]
                         [0]["id"], self.user.id)

    # 15. update a user
    def test_update_user(self):
        """
        Ensure we can update a user object.
        """
        # the full record is required for the POST
        data = {
            "id": 115,
            "password": "123_Pass*",
            "last_login": "2024-04-10 10:11:12",
            "is_superuser": "False",
            "username": "The Bestest",
            "last_name": "Parent",
            "email": "thebestest@gmail.com",
            "is_staff": "False",
            "is_active": "True",
            "date_joined": "2024-04-15 05:01:03",
            "first_name": "Female"
        }
        response = self.client.put(
            reverse("barkyapi:user-detail",
                    kwargs={"pk": self.user.id}),
            data,
            format="json",
        )
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["username"], "The Bestest")


class OtherTests(APITestCase):
    # 16. highlight a snippet
    def test_highlight_snippets(self):
        """
        Ensure we can highlight snippet objects.
        """
        data = SnippetSerializer()

        response = SnippetViewSet.highlight(self, data)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"]["title"], self.snippet.title)

    # 17. list bookmarks by user


    # 18. list snippets by user
'''
    def test_list_snippets_by_user(self, criteria):
        """
        Ensure we can list all snippet objects for a user.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"]
                         [0]["title"], self.snippet.title)
'''
# 20. list bookmarks by date
# 21. list snippets by date
# 23. list bookmarks by title
# 24. list snippets by title
# 26. list bookmarks by url
# 27. list snippets by url
