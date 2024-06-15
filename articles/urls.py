from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, TagViewSet, IncrementViews

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('articles/<uuid:pk>/increment-views/', IncrementViews.as_view(), name='increment-views'),
]
