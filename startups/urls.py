from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StartupViewSet, RatingViewSet, GetRatingId, StartupAverageRating, StartupComments, GetCommentId, \
    CommentViewSet, IncrementViews, TransactionView, CategoryViewSet

router = DefaultRouter()
router.register(r'startups', StartupViewSet)
router.register(r'ratings', RatingViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ratings/user/<uuid:user_id>/startup/<uuid:startup_id>/get_rating_id/', GetRatingId.as_view(),
         name='get_rating_id'),
    path('ratings/startup/<uuid:startup_id>/average_rating/', StartupAverageRating.as_view(),
         name='startup_average_rating'),
    path('comments/startup/<uuid:startup_id>/', StartupComments.as_view(), name='startup_comments'),
    path('comments/user/<uuid:user_id>/startup/<uuid:startup_id>/', GetCommentId.as_view(), name='get_comment_id'),
    path('startups/<uuid:pk>/increment-views/', IncrementViews.as_view(), name='increment-views'),
    path('transaction/', TransactionView.as_view(), name='transaction'),
]
