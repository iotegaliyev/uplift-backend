from django.contrib import admin
from .models import Startup, Rating, Comment, Category

# Register your models here.
admin.site.register(Startup)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Category)