import pytz
import uuid

from django.db import models
from django.utils import timezone

from users.models import CustomUser


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

    def __str__(self):
        return self.name


class Startup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='startups/', null=True, blank=True)
    founder = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    goal = models.DecimalField(max_digits=10, decimal_places=2)
    founded_date = models.DateField(auto_now_add=True)
    remaining_days = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    collected = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    views = models.FloatField(default=0)

    def increment_views(self):
        self.views += 1
        self.save()

    def update_remaining_days(self):
        if self.is_active:
            oral_tz = pytz.timezone('Asia/Oral')
            utc_now = timezone.now()
            oral_now = utc_now.astimezone(oral_tz)
            oral_today = oral_now.date()
            delta = oral_today - self.founded_date
            self.remaining_days = max(30 - delta.days, 0)
            if self.remaining_days == 0:
                self.is_active = False
            self.save()
            return self.remaining_days
        else:
            return 0

    def __str__(self):
        return self.name


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, null=True, blank=True)
    value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'startup')

    def __str__(self):
        return f"{self.user.username} - {self.startup.name}: {self.value}"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.startup.name}: {self.comment}"
