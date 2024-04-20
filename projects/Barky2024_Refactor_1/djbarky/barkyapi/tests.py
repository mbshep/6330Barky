from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework import routers
from rest_framework.test import APIRequestFactory, APITestCase

from .models import Bookmark, Snippet
from .views import BookmarkViewSet, SnippetViewSet

# Create your tests here.
# test plan


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
        self.factory = APIRequestFactory()
        self.snippet = Snippet.objects.create(
            created="04/15/2024",
            title="Awesome snippet",
            code="example awesome snippet code",
            linenos="False",
            language="python",
            style="friendly",
            owner="admin",
            highlighted="code",
        )
        # print(f"snippet id: {self.snippet.id}")

        # the simple router provides the name 'snippet-list' for the URL pattern: https://www.django-rest-framework.org/api-guide/routers/#simplerouter
        self.list_url = reverse("barkyapi:snippet-list")
        self.detail_url = reverse(
            "barkyapi:snippet-detail", kwargs={"pk": self.snippet.id}
        )
    # 6. create a snippet

    def test_create_snippet(self):
        """
        Ensure we can create a new snippet object.
        """

        # the full record is required for the POST
        data = {
            "created": "04/20/2024",
            "title": "Django REST framework",
            "code": "example snippet code",
            "linenos": "False",
            "language": "python",
            "style": "friendly",
            "owner": "admin",
            "highlighted": "code",
        }
        response = self.client.post(self.list_url, data, format="json")
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(Snippet.objects.count(), 2)
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
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Snippet.objects.count(), 0)

    # 9. list snippets
    def test_list_snippets(self):
        """
        Ensure we can list all snippet objects.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"]
                         [0]["title"], self.snippet.title)

    # 10. update a snippet
    def test_update_snippet(self):
        """
        Ensure we can update a snippet object.
        """
        # the full record is required for the POST
        data = {
            "created": "04/21/2024",
            "title": "Even better Django",
            "code": "example snippet code",
            "linenos": "False",
            "language": "python",
            "style": "friendly",
            "owner": "admin",
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
    # 11. create a user

    # 12. retrieve a user

    # 13. delete a user

    # 14. list users

    # 15. update a user

    # 16. highlight a snippet

    # 17. list bookmarks by user

    # 18. list snippets by user
    def test_list_snippets_by_user(self, criteria):
        """
        Ensure we can list all snippet objects for a user.
        """
        response = self.client.get(self.list_url)
        self.assertTrue(status.is_success(response.status_code))
        self.assertEqual(response.data["results"]
                         [0]["title"], self.snippet.title)

    # 20. list bookmarks by date
    # 21. list snippets by date
    # 23. list bookmarks by title
    # 24. list snippets by title
    # 26. list bookmarks by url
    # 27. list snippets by url
