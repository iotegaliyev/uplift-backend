from .views import RegisterView, LoginView
from django.urls import path, include
from .views import ProfileByUserId, UserViewSet, ProfileViewSet, UserArticlesView, UserStartupsView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(router.urls)),
    path('profile/<uuid:user_id>/', ProfileByUserId.as_view(), name='profile_by_user_id'),
    path('profile/my-articles/', UserArticlesView.as_view(), name='user-articles'),
    path('profile/my-startups/', UserStartupsView.as_view(), name='user-startups'),
]
