from django.test import TestCase
from django.urls import reverse
from .models import Post
from bs4 import BeautifulSoup
import requests

create_post = Post.objects.create


class ParserTests(TestCase):
    url = "https://news.ycombinator.com/"

    def test_fetch_posts(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)
        bs = BeautifulSoup(response.text, "html.parser")
        data = [
            {
                "url": k["href"],
                "title": k.get_text()
            } for k
            in bs.find_all("a", attrs={"class": "storylink"})
        ]
        self.assertTrue(data)
        self.assertTrue(data[0]["url"])
        self.assertTrue(data[0]["title"])


class PostsViewTests(TestCase):
    url = reverse("posts:list")

    def setUp(self):
        for i in range(1, 50):
            create_post(title="title%s" % i, url="https://testing%s.com" % i)

    def test_view_posts_default(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 5)

        self.assertTrue(response.json()[0]["id"] == 1)
        self.assertTrue(response.json()[0]["title"] == "title1")
        self.assertURLEqual(response.json()[0]["url"], "https://testing1.com")
        self.assertIn("created", response.json()[0])

    def test_view_posts_order(self):
        response = self.client.get(self.url + "?order=not_existed_field")
        self.assertDictEqual(
            response.json(),
            {'error': 'Ordering attribute not_existed_field does not exist'})

        response = self.client.get(self.url + "?order=title")
        self.assertTrue(response.json()[0]["title"] == "title1")

        response = self.client.get(self.url + "?order=-title")
        self.assertTrue(response.json()[0]["title"] == "title9")

    def test_view_posts_offset(self):
        for offset in (-1, "bla"):
            response = self.client.get(self.url + "?offset=%s" % offset)
            self.assertDictEqual(
                response.json(), {"error": "Offset %s is not valid" % offset})

        response = self.client.get(self.url + "?offset=25")
        self.assertListEqual(
            [k["id"] for k in response.json()], [26, 27, 28, 29, 30])

        response = self.client.get(self.url + "?offset=100")
        self.assertListEqual(response.json(), [])

    def test_view_posts_limit(self):
        for limit in (-1, "bla"):
            response = self.client.get(self.url + "?limit=%s" % limit)
            self.assertDictEqual(
                response.json(), {"error": "Limit %s is not valid" % limit})

        response = self.client.get(self.url + "?limit=25")
        self.assertTrue(len(response.json()) == 25)
