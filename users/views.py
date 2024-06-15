from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from .serializers import CustomUserSerializer, ProfileSerializer
from startups.serializers import StartupSerializer
from articles.serializers import ArticleSerializer
from .models import CustomUser, Profile
from .utils import send_welcome_email
from startups.models import Startup
from articles.models import Article


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_welcome_email(user.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    pass


class ProfileByUserId(APIView):
    def get(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({"error": "User does not exist"}, status=404)
        except Profile.DoesNotExist:
            return Response({"error": "Profile does not exist for this user"}, status=404)


class UserArticlesView(generics.ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        user = self.request.user
        return Article.objects.filter(author=user)


class UserStartupsView(generics.ListAPIView):
    serializer_class = StartupSerializer

    def get_queryset(self):
        user = self.request.user
        return Startup.objects.filter(founder=user)
