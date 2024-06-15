import uuid
from django.db import models
from users.models import CustomUser


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0, null=True, blank=True)

    def increment_views(self):
        self.views += 1
        self.save()

    def __str__(self):
        return self.title
