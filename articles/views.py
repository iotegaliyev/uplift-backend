from rest_framework import viewsets
from .models import Article, Tag
from .serializers import ArticleSerializer, TagSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IncrementViews(APIView):

    def post(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
            article.increment_views()
            serializer = ArticleSerializer(article)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Article.DoesNotExist:
            return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)

