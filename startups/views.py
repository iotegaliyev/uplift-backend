from rest_framework import viewsets
from rest_framework.response import Response
from .models import Startup, Rating, Comment, Category
from .serializers import StartupSerializer, RatingSerializer, TransactionSerializer, CommentReadSerializer, \
    CommentWriteSerializer, CategorySerializer, StartupCreateSerializer
from rest_framework import status
from django.db.models import Avg
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from users.models import Profile


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class StartupViewSet(viewsets.ModelViewSet):
    queryset = Startup.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return StartupCreateSerializer
        return StartupSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_remaining_days()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Update remaining days for each startup in the queryset
        for startup in queryset:
            startup.update_remaining_days()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class GetRatingId(APIView):
    def get(self, request, user_id, startup_id):
        try:
            rating = Rating.objects.get(user_id=user_id, startup_id=startup_id)
            return Response({'rating_id': rating.id}, status=status.HTTP_200_OK)
        except Rating.DoesNotExist:
            return Response({'error': 'Rating not found'}, status=status.HTTP_404_NOT_FOUND)


class StartupAverageRating(APIView):
    def get(self, request, startup_id):
        try:
            average_rating = Rating.objects.filter(startup_id=startup_id).aggregate(Avg('value'))['value__avg']
            if average_rating is not None:
                return Response({'average_rating': average_rating}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No ratings found for this startup'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CommentReadSerializer
        return CommentWriteSerializer


class StartupComments(APIView):
    def get(self, request, startup_id):
        try:
            comments = Comment.objects.filter(startup_id=startup_id)
            serializer = CommentReadSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetCommentId(APIView):
    def get(self, request, user_id, startup_id):
        try:
            comment = Comment.objects.get(user_id=user_id, startup_id=startup_id)
            return Response({'comment_id': comment.id}, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)


class IncrementViews(APIView):

    def post(self, request, pk):
        try:
            startup = Startup.objects.get(pk=pk)
            startup.increment_views()
            serializer = StartupSerializer(startup)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Startup.DoesNotExist:
            return Response({'error': 'Startup not found'}, status=status.HTTP_404_NOT_FOUND)


class TransactionView(APIView):
    @swagger_auto_schema(request_body=TransactionSerializer)
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            startup_id = serializer.validated_data['startup_id']
            user_id = serializer.validated_data['user_id']
            amount = serializer.validated_data['amount']

            profile = get_object_or_404(Profile, user=user_id)
            startup = get_object_or_404(Startup, id=startup_id)

            if profile.balance < amount:
                return Response({"detail": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

            profile.balance -= amount
            startup.collected += amount

            profile.save()
            startup.save()

            return Response({"detail": "Transaction successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
