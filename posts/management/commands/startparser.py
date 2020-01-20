from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from posts.models import Post
from bs4 import BeautifulSoup
import requests


class Command(BaseCommand):
    help = "Fetch posts from HackerNews and save them in local database"
    url = "https://news.ycombinator.com/"

    def _fetch_data(self):
        def transform_link(link):
            if link.startswith("http://") or link.startswith("https://"):
                return link
            return self.url.rstrip("/") + "/" + link
        response = requests.get(self.url)
        response.encoding = "utf-8"
        bs = BeautifulSoup(response.text, "html.parser")
        return [
            {
                "url": transform_link(k["href"]),
                "title": k.get_text()
            } for k
            in bs.find_all("a", attrs={"class": "storylink"})
        ]

    def handle(self, *args, **options):
        count = 0
        for d in self._fetch_data():
            try:
                Post.objects.create(url=d["url"], title=d["title"])
                self.stdout.write("* " + self.style.SUCCESS(d["title"]))
                count += 1
            except IntegrityError:
                self.stdout.write("* " + self.style.ERROR(d["title"]))
        self.stdout.write(self.style.SUCCESS(
            "{} new posts was saved.".format(count)))
