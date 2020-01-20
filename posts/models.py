from django.db import models
from django.utils.timezone import now


class Post(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    created = models.DateTimeField(default=now)

    def __str__(self):
        return self.title
